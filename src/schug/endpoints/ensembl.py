from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from schug.database import get_session
from schug.models import EnsemblGene, EnsemblGeneRead
from schug.models import EnsemblTranscript, EnsemblTranscriptRead
from sqlmodel import Session, select

router = APIRouter()


@router.get("/", response_model=List[EnsemblGeneRead])
def read_ensembl_genes(
        *,
        session: Session = Depends(get_session),
        limit: int = Query(default=100, lte=100),
):
    ensembl_genes = session.exec(select(EnsemblGene).limit(limit)).all()
    return ensembl_genes


@router.get("/{ensembl_gene_id}", response_model=List[EnsemblTranscriptRead])
def read_ensembl_transcripts(
        *,
        ensembl_gene_id: str,
        session: Session = Depends(get_session),
        limit: int = Query(default=100, lte=100),
        only_canonical: Optional[bool] = False
):
    where_clause = select(EnsemblTranscript).where(EnsemblTranscript.ensembl_gene_id == ensembl_gene_id)
    if only_canonical:
        where_clause = where_clause.where(EnsemblTranscript.is_canonical)

    ensembl_transcripts = session.exec(where_clause.limit(limit)).all()
    return ensembl_transcripts
