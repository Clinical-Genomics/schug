from typing import List

from fastapi import APIRouter, Depends, Query, status
from .http_exceptions import SchugHttpException
from schug.database.session import get_session
from schug.models import Gene, GeneRead
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
    SchugHttpException.error_404(result=genes, query="Ensembl Genes")
    return genes


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
