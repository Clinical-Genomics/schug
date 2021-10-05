import csv
from typing import List

import typer
from pydantic import parse_obj_as
from schug.models.exon import EnsemblExon
from schug.models.gene import EnsemblGene
from schug.models.transcript import EnsemblTranscript

app = typer.Typer()


@app.command()
def exons(exons_file: typer.FileText = typer.Option(None, "--infile", "-i")):
    """Load exon data"""
    typer.echo("Loading exons")

    parsed_exons = parse_obj_as(
        List[EnsemblExon],
        [parsed_line for parsed_line in csv.DictReader(exons_file, delimiter="\t")],
    )
    for i, exon in enumerate(parsed_exons):
        if i == 5:
            break
        typer.echo(exon)


@app.command()
def transcripts(transcripts_file: typer.FileText = typer.Option(None, "--infile", "-i")):
    """Load transcript data"""
    typer.echo("Loading transcripts")

    parsed_transcripts = parse_obj_as(
        List[EnsemblTranscript],
        [parsed_line for parsed_line in csv.DictReader(transcripts_file, delimiter="\t")],
    )
    for i, tx in enumerate(parsed_transcripts):
        if i == 5:
            break
        typer.echo(tx)


@app.command()
def genes(ensembl_file: typer.FileText = typer.Option(None, "--infile", "-i")):
    """Load transcript data"""
    typer.echo("Loading genes")

    parsed_genes = parse_obj_as(
        List[EnsemblGene],
        [parsed_line for parsed_line in csv.DictReader(ensembl_file, delimiter="\t")],
    )
    for i, gene in enumerate(parsed_genes):
        if i == 5:
            break
        typer.echo(gene)


@app.command()
def hgnc(ensembl_file: typer.FileText = typer.Option(None, "--infile", "-i")):
    """Load transcript data"""
    typer.echo("Parsing genes")
    from pprint import pprint

    for i, gene in enumerate(csv.DictReader(ensembl_file, delimiter="\t")):
        if i == 5:
            break
        pprint(gene)
