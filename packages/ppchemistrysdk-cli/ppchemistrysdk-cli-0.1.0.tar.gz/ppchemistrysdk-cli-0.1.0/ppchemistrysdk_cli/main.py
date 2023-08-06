"""Command-line interface for PPChemistrySDK-CLI."""
import typer

try:
    import ppchemsdk as chem
except ImportError:
    typer.echo("Biovia PPChemistrySDK python library needs to be installed.")

# initialize App
app = typer.Typer()


@app.callback()
def callback():
    """
    Command-line interface for the PPChemistrySDK python package.
    """


@app.command()
def formula(smiles: str):
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
    molecular_formular = property.getMolecularFormula(mol, True)
    typer.echo(molecular_formular)


@app.command()
def composition(smiles: str):
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
    molecular_composition = property.getMolecularComposition(mol)
    typer.echo(molecular_composition)


@app.command()
def weight(smiles: str):
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
    molecular_weight = property.getMolecularWeight(mol)
    typer.echo(molecular_weight)


@app.command()
def mass(smiles: str):
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
    molecular_mass = property.getMolecularMass(mol)
    typer.echo(molecular_mass)


@app.command()
def volume(smiles: str):
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
    molecular_volume = property.getDSFastVolume(mol)
    typer.echo(molecular_volume)


@app.command()
def surface(smiles: str):
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
    molecular_surface = property.getSurfaceArea(mol)
    typer.echo(molecular_surface)


@app.command()
def gasteiger_charges(smiles: str):
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
    atomic_charges = property.getGasteigerCharges(mol)
    typer.echo(atomic_charges)


@app.command()
def inchi_key(smiles: str):
    """
    Get InChI key from a SMILES string.

    Args:
    smiles: SMILES string (str)

    Returns:
    InChI key.
    """
    molIO = chem.MolIO()
    mol = chem.Molecule()
    property = chem.MolPropCalc()
    molIO.readMolecule(smiles, chem.MolIO.FormatType.SMILES_String, mol)
    inchi_key = property.getInChI(mol)
    typer.echo(inchi_key.getInChI())


@app.command()
def nema_key(smiles: str):
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
    nema_key = property.getNEMAKey(mol)
    typer.echo(nema_key)


@app.command()
def alogP(smiles: str):
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
    alogP = property.getAlogP(mol)
    typer.echo(alogP)


@app.command()
def ref(smiles: str):
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
    molecular_ref = property.getMolRef(mol)
    typer.echo(molecular_ref)


@app.command()
def rotational_bonds(smiles: str):
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
    number_rotational_bonds = property.getNumRotatableBonds(mol)
    typer.echo(number_rotational_bonds)


@app.command()
def donors(smiles: str):
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
    number_donors = property.getNumDonors(mol)
    typer.echo(number_donors)


@app.command()
def acceptors(smiles: str):
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
    number_acceptors = property.getNumAcceptors(mol)
    typer.echo(number_acceptors)


@app.command()
def lipinski_donors(smiles: str):
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
    number_lipinski_donors = property.getNumLipinskiDonors(mol)
    typer.echo(number_lipinski_donors)


@app.command()
def lipinski_acceptors(smiles: str):
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
    number_lipinski_acceptors = property.getNumLipinskiAcceptors(mol)
    typer.echo(number_lipinski_acceptors)


@app.command()
def lipinski_violations(smiles: str):
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
    number_lipinski_violations = property.getNumLipinskiViolations(mol)
    typer.echo(number_lipinski_violations)
