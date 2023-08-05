# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

##
# Module for the Molecule class for defining and visualizing molecules
##
import enum
import logging
import os
import re

from collections import namedtuple
from IPython.display import display
from typing import List, Dict

try:
    from rdkit.Chem import AllChem as Chem
except ImportError as e:
    raise ImportError("Missing dependency: rdkit. \
Install with Conda: \n\n\tconda install -c conda-forge rdkit")

from qdk.chemistry.widgets.jsmol_widget import JsmolWidget
from qdk.chemistry.widgets.jsme_widget import JsmeWidget
from qdk.chemistry.geometry import Geometry
from qdk.chemistry.solvers import nwchem, openmolcas, psi4
from qdk.chemistry._xyz2mol import xyz2mol, read_xyz_file
from qdk.chemistry.solvers.util import num_electrons

import basis_set_exchange as bse

_log = logging.getLogger(__name__)

DEFAULT_BASE_PATH = os.environ.get("QDKCHEM_OUTPUT_PATH", ".")
SolverSpec = namedtuple("SolverSpec", ["name", "module", "extension"])


class Solver(enum.Enum):
    nwchem = SolverSpec(
        name="NWChem",
        module=nwchem,
        extension=".nw"
    )
    openmolcas = SolverSpec(
        name="OpenMolcas",
        module=openmolcas,
        extension=".inp"
    )
    psi4 = SolverSpec(
        name="Psi4",
        module=psi4,
        extension=".in"
    )


class Molecule(object):
    """
    Molecule object for visualization and geometry generation
    """
    def __init__(self, mol: Chem.Mol, num_confs: int = 10, xyz: str = None):
        self.mol = mol
        self.design_widget = None
        self._xyz = xyz

        if xyz:
            self.widget = JsmolWidget.from_str(data=xyz)
        elif mol:
            self.widget = JsmolWidget.from_mol(mol=mol, num_confs=num_confs)
        else:
            self.widget = None

    @classmethod
    def from_smiles(
        cls,
        smiles: str,
        add_hs: bool = True,
        num_confs: int = 10
    ):
        mol = Chem.MolFromSmiles(smiles)
        if add_hs:
            mol = Chem.AddHs(mol)
            # Calculate conformers after adding hydrogens
            Chem.EmbedMultipleConfs(mol, numConfs=num_confs)

        return cls(mol=mol)

    @classmethod
    def from_xyz(cls, xyz_file: str, add_hs: bool = True):
        atoms, charge_read, coordinates = read_xyz_file(xyz_file)
        mols = xyz2mol(atoms, coordinates, charge=charge_read)
        with open(xyz_file) as f:
            xyz = f.read()

        _log.info(f"Generated {len(mols)} molecules.")

        if len(mols) > 0:
            mol = mols[0]
            return cls(mol=mol, xyz=xyz)

        else:
            raise IOError("Error creating molecule object from XYZ file: no \
molecules generated by xyz2mol.")

    @property
    def geometry(self):
        if self._xyz:
            return Geometry.from_xyz(self._xyz)
        return Geometry.from_mol(self.mol)

    def xyz(self, name: str = "unnamed"):
        if self._xyz:
            return self._xyz
        return self.geometry.to_xyz(title=name)

    @property
    def smiles(self):
        """Convert RDKit molecule to canonical Smiles string"""
        from rdkit.Chem import AllChem as Chem
        return Chem.MolToSmiles(Chem.RemoveHs(self.mol))

    @property
    def num_electrons(self):
        """Get the number of electrons for the molecule"""
        return num_electrons(self.mol)

    def all_atoms(self):
        return [atom.GetAtomicNum() for atom in self.mol.GetAtoms()]

    @property
    def atoms(self) -> List[int]:
        return sorted(set(self.all_atoms()))

    @property
    def atom_numbers(self) -> Dict[int, int]:
        """Get a dictionary of the atomic numbers of atoms in the molecule
        mapped to the amount of each in the molecule"""
        atoms = self.all_atoms()
        return {
            atomic_number:
                atoms.count(atomic_number) for atomic_number in set(atoms)
        }

    def basis(self, basis: str = "STO-3G"):
        # Obtain the basis set in nwchem format (as a string)
        atoms = self.atoms
        basis = bse.get_basis(basis, elements=atoms, fmt='nwchem')
        ob = "d*[spdf]"
        parsed_basis = re.findall(
            f"-> \\[(\\{ob},*\\{ob}*,*\\{ob}*)\\]\n(\\w+)",
            basis
        )
        assert len(atoms) == len(parsed_basis), \
            f"Cannot parse basis: number of atoms does not match result: \
{basis}"
        return dict(zip(atoms, parsed_basis))

    def num_orbitals(self, basis: str = "STO-3G") -> int:
        """Get total number of spatial orbitals for the molecule by
        using the basis states"""
        pattern = "(\\d)*s*,*(\\d)*p*,*(\\d)*d*,*(\\d)*f*"
        orbital_fillings = [1, 3, 5, 7]

        spin_orbitals = 0
        for atom, (basis, name) in self.basis(basis).items():
            num_atoms = self.atom_numbers[atom]
            s, p, d, f = re.findall(pattern, basis)[0]

            num_electrons_per_orbital = [
                filling * int(num) for num, filling in zip(
                    [s, p, d, f],
                    orbital_fillings
                ) if num
            ]
            num_electrons_per_atom = sum(num_electrons_per_orbital)
            spin_orbitals += num_atoms * num_electrons_per_atom

        return int(spin_orbitals)

    @classmethod
    def design(cls):
        from varname import varname, VarnameRetrievingError
        try:
            name = varname()
        except VarnameRetrievingError:
            name = "_"

        mol = cls(mol=None)
        mol.design_widget = JsmeWidget(parent_varname=name)
        mol._updated = True
        display(mol.design_widget)
        return mol

    def update_design(self, add_hs: bool = True, num_confs: int = 10):
        mol = self.design_widget.to_mol(add_hs=add_hs)
        self.mol = mol
        self.widget = JsmolWidget.from_mol(mol=mol, num_confs=num_confs)

    def create_input(
        self,
        molecule_name: str,
        file_name: str,
        solver: str,
        base_path: str = None,
        **parameters
    ):
        """Create input deck and save to file

        :param molecule_name: Name of the input deck
        :type molecule_name: str
        :param file_name: Output file name
        :type file_name: str
        :param solver: Solver to use
        :type solver: str
        :param base_path: Path to save output file to
        :type base_path: str
        :param parameters: Parameters for input deck
        :type parameters: dict
        """
        try:
            solver_spec = Solver[solver.lower()].value

        except Exception:
            names = [_s.name for _s in Solver]
            raise ValueError(
                f"Solver {solver} not found. Valid values: {names}"
            )

        else:
            if base_path is None:
                base_path = DEFAULT_BASE_PATH

            file_path = os.path.join(base_path, file_name)

            input_deck = solver_spec.module.create_input_deck(
                mol=self.mol,
                mol_name=molecule_name,
                geometry=self.geometry,
                **parameters
            )

            _log.info(
                f"Saving {solver_spec.name} input deck to file {file_path}"
            )
            with open(file_path, "w") as f:
                f.write(input_deck)

            return file_path

    def _ipython_display_(self):
        if self.design_widget and self.design_widget.was_updated:
            self.update_design()
            self.design_widget.reset_updated()

        return display(self.widget)
