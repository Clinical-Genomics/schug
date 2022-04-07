import csv
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status, HTTPException

from .http_exceptions import SchugHttpException
from schug.database.genes import create_gene_item
from schug.database.session import get_session
from schug.load.ensemble import (
    fetch_ensembl_genes,
)
from schug.models import Gene, GeneRead, GeneCreate, EnsemblGene

from pydantic import parse_obj_as

from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

router = APIRouter()


@router.get("/", response_model=List[GeneRead])
def read_genes(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    genes = session.exec(select(Gene).offset(offset).limit(limit)).all()
    SchugHttpException.error_404(result=genes, query="genes")
    return genes


@router.post("/", response_model=List[GeneCreate])
def create_genes(
        *,
        session: Session = Depends(get_session),
        build: Optional[str] = "38",
        chromosome: Optional[str] = "Y",
):
    ensembl_obj = fetch_ensembl_genes(build=build, chromosomes=chromosome)

    parsed_genes = parse_obj_as(
        List[EnsemblGene],
        [parsed_line for parsed_line in csv.DictReader(ensembl_obj, delimiter="\t")],
    )

    genes_created = []
    for i, gene in enumerate(parsed_genes):
        if i == 5:
            break
        gene.genome_build = build
        genes_created.append(create_gene_item(ensembl_gene=gene, session=session))
    return genes_created


@router.delete("/")
def delete_genes(
        session: Session = Depends(get_session)
):
    genes = session.exec(select(Gene)).all()
    SchugHttpException.error_404(result=genes, query="gene entries")
    for gene in genes:
        session.delete(gene)
        session.commit()

    return {"Gene table cleared"}


@router.get("/{db_id}", response_model=GeneRead)
def read_gene_db_id(
    *,
    db_id: int,
    session: Session = Depends(get_session),
):
    gene = session.get(Gene, db_id)
    if not gene:
        SchugHttpException.error_404(result=gene, query=db_id)
    return gene


@router.get("/hgnc_id/{hgnc_id}", response_model=GeneRead)
def read_gene_hgnc_id(
    *,
    hgnc_id: int,
    session: Session = Depends(get_session),
):
    try:
        gene = session.exec(select(Gene).where(Gene.hgnc_id == hgnc_id)).one()
    except NoResultFound:
        SchugHttpException.error_404(result=None, query=hgnc_id)
    return gene


@router.get("/hgnc_symbol/{hgnc_symbol}", response_model=GeneRead)
def read_gene_hgnc_symbol(
    *,
    hgnc_symbol: str,
    session: Session = Depends(get_session),
):
    try:
        gene = session.exec(select(Gene).where(Gene.primary_symbol == hgnc_symbol)).one()
    except NoResultFound:
        SchugHttpException.error_404(result=None, query=hgnc_symbol)
    return gene
