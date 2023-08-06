"""Core functionalities for usage as package."""
import typer

try:
    import ppchemsdk as chem
except ImportError:
    typer.echo("Biovia PPChemistrySDK python library needs to be installed.")


def acceptors(smiles: str) -> int:
    """
    Get number of acceptors from a SMILES string.

    Args:
    smiles: SMILES string (str)

    Returns:
    Number of acceptors.
    """
    molIO = chem.MolIO()
    mol = chem.Molecule()
    property = chem.MolPropCalc()
    molIO.readMolecule(smiles, chem.MolIO.FormatType.SMILES_String, mol)
    return property.getNumAcceptors(mol)


def alogP(smiles: str) -> float:
    """
    Get molecular alogP from a SMILES string.

    Args:
    smiles: SMILES string (str)

    Returns:
    Molecular alogP.
    """
    molIO = chem.MolIO()
    mol = chem.Molecule()
    property = chem.MolPropCalc()
    molIO.readMolecule(smiles, chem.MolIO.FormatType.SMILES_String, mol)
    return property.getAlogP(mol)


def formula(smiles: str) -> str:
    """
    Get the moelcular formular from a SMILES string.

    Args:
    smiles: SMILES string (str)

    Returns:
    Molecular formular.
    """
    molIO = chem.MolIO()
    mol = chem.Molecule()
    property = chem.MolPropCalc()
    molIO.readMolecule(smiles, chem.MolIO.FormatType.SMILES_String, mol)
    return property.getMolecularFormula(mol, True)


def composition(smiles: str) -> str:
    """
    Get the molecular composition from a SMILES string.

    Args:
    smiles: SMILES string (str)

    Returns:
    Molecular composition.
    """
    molIO = chem.MolIO()
    mol = chem.Molecule()
    property = chem.MolPropCalc()
    molIO.readMolecule(smiles, chem.MolIO.FormatType.SMILES_String, mol)
    return property.getMolecularComposition(mol)


def donors(smiles: str) -> int:
    """
    Get number of donors from a SMILES string.

    Args:
    smiles: SMILES string (str)

    Returns:
    Number of donors.
    """
    molIO = chem.MolIO()
    mol = chem.Molecule()
    property = chem.MolPropCalc()
    molIO.readMolecule(smiles, chem.MolIO.FormatType.SMILES_String, mol)
    return property.getNumDonors(mol)


def gasteiger_charges(smiles: str) -> list:
    """
    Get the atomic Gasteiger partial charges from a SMILES string.

    Args:
    smiles: SMILES string (str)

    Returns:
    Atomic Gasteiger partial charges.
    """
    molIO = chem.MolIO()
    mol = chem.Molecule()
    property = chem.MolPropCalc()
    molIO.readMolecule(smiles, chem.MolIO.FormatType.SMILES_String, mol)
    return property.getGasteigerCharges(mol)


def inchi_key(smiles: str) -> str:
    """
    Get InChI key from a SMILES string.

    Args:
    smiles: SMILES string (str)

    Returns:
    InChI key object.
    """
    molIO = chem.MolIO()
    mol = chem.Molecule()
    property = chem.MolPropCalc()
    molIO.readMolecule(smiles, chem.MolIO.FormatType.SMILES_String, mol)
    return property.getInChI(mol).getInChI()


def lipinski_acceptors(smiles: str) -> int:
    """
    Get number of Lipinski acceptors from a SMILES string.

    Args:
    smiles: SMILES string (str)

    Returns:
    Number of Lipinski acceptors.
    """
    molIO = chem.MolIO()
    mol = chem.Molecule()
    property = chem.MolPropCalc()
    molIO.readMolecule(smiles, chem.MolIO.FormatType.SMILES_String, mol)
    return property.getNumLipinskiAcceptors(mol)


def lipinski_donors(smiles: str) -> int:
    """
    Get number of Lipinski donors from a SMILES string.

    Args:
    smiles: SMILES string (str)

    Returns:
    Number of Lipinski donors.
    """
    molIO = chem.MolIO()
    mol = chem.Molecule()
    property = chem.MolPropCalc()
    molIO.readMolecule(smiles, chem.MolIO.FormatType.SMILES_String, mol)
    return property.getNumLipinskiDonors(mol)


def lipinski_violations(smiles: str) -> int:
    """
    Get number of Lipinski violations from a SMILES string.

    Args:
    smiles: SMILES string (str)

    Returns:
    Number of Lipinski violations.
    """
    molIO = chem.MolIO()
    mol = chem.Molecule()
    property = chem.MolPropCalc()
    molIO.readMolecule(smiles, chem.MolIO.FormatType.SMILES_String, mol)
    return property.getNumLipinskiViolations(mol)


def mass(smiles: str) -> float:
    """
    Get the molecular mass from a SMILES string.

    Args:
    smiles: SMILES string (str)

    Returns:
    Molecular mass.
    """
    molIO = chem.MolIO()
    mol = chem.Molecule()
    property = chem.MolPropCalc()
    molIO.readMolecule(smiles, chem.MolIO.FormatType.SMILES_String, mol)
    return property.getMolecularMass(mol)


def nema_key(smiles: str) -> str:
    """
    Get Nema key from a SMILES string.

    Args:
    smiles: SMILES string (str)

    Returns:
    Nema key.
    """
    molIO = chem.MolIO()
    mol = chem.Molecule()
    property = chem.MolPropCalc()
    molIO.readMolecule(smiles, chem.MolIO.FormatType.SMILES_String, mol)
    return property.getNEMAKey(mol)


def ref(smiles: str) -> float:
    """
    Get molecular reference from a SMILES string.

    Args:
    smiles: SMILES string (str)

    Returns:
    Molecular reference.
    """
    molIO = chem.MolIO()
    mol = chem.Molecule()
    property = chem.MolPropCalc()
    molIO.readMolecule(smiles, chem.MolIO.FormatType.SMILES_String, mol)
    return property.getMolRef(mol)


def rotational_bonds(smiles: str) -> int:
    """
    Get number of rotational bonds from a SMILES string.

    Args:
    smiles: SMILES string (str)

    Returns:
    Number of rotational bonds.
    """
    molIO = chem.MolIO()
    mol = chem.Molecule()
    property = chem.MolPropCalc()
    molIO.readMolecule(smiles, chem.MolIO.FormatType.SMILES_String, mol)
    return property.getNumRotatableBonds(mol)


def surface(smiles: str) -> float:
    """
    Get the molecular surface from a SMILES string.

    Args:
    smiles: SMILES string (str)

    Returns:
    Molecular surface.
    """
    molIO = chem.MolIO()
    mol = chem.Molecule()
    property = chem.MolPropCalc()
    molIO.readMolecule(smiles, chem.MolIO.FormatType.SMILES_String, mol)
    return property.getSurfaceArea(mol)


def volume(smiles: str) -> float:
    """
    Get the molecular volume from a SMILES string.

    Args:
    smiles: SMILES string (str)

    Returns:
    Molecular volume.
    """
    molIO = chem.MolIO()
    mol = chem.Molecule()
    property = chem.MolPropCalc()
    molIO.readMolecule(smiles, chem.MolIO.FormatType.SMILES_String, mol)
    return property.getDSFastVolume(mol)


def weight(smiles: str) -> float:
    """
    Get the molecular weight from a SMILES string.

    Args:
    smiles: SMILES string (str)

    Returns:
    Molecular weight.
    """
    molIO = chem.MolIO()
    mol = chem.Molecule()
    property = chem.MolPropCalc()
    molIO.readMolecule(smiles, chem.MolIO.FormatType.SMILES_String, mol)
    return property.getMolecularWeight(mol)
