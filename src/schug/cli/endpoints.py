import typer

from schug.load.ensemble import fetch_ensembl_genes
from schug.models.ensembl import EnsemblGeneCreate
from schug.database.ensembl import put_ensembl_gene

app = typer.Typer()


@app.command()
def ensembl_genes(build: str = typer.Option("38", "-b", "--build")):
    """Fetch from Ensembl client"""
    ensembl_client = fetch_ensembl_genes(build=build, chromosomes=["Y"])
    for i, line in enumerate(ensembl_client):
        line = f"{line}\t{build}".split("\t")
        created_gene = EnsemblGeneCreate(
            chromosome=line[0],
            start=line[1],
            end=line[2],
            ensembl_id=line[3],
            genome_build=build,
        )
        if i == 15:
            break
        typer.echo(put_ensembl_gene(created_gene))
