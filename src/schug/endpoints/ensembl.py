from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from schug.database import get_session
from schug.models import EnsemblGene, EnsemblGeneRead
from schug.models import EnsemblTranscript, EnsemblTranscriptRead
from sqlmodel import Session, select

router = APIRouter()


@router.get("/", response_model=List[EnsemblGeneRead])
def read_ensembl_genes(
        session: Session = Depends(get_session),
        limit: int = Query(default=100, lte=100),
) -> list[EnsemblGeneRead]:
    """Get all ensembl genes from the database"""
    ensembl_genes = session.exec(select(EnsemblGene).limit(limit)).all()
    return ensembl_genes


@router.get("/{ensembl_gene_id}", response_model=List[EnsemblTranscriptRead])
def read_ensembl_transcripts(
        ensembl_gene_id: str,
        session: Session = Depends(get_session),
        limit: int = Query(default=100, lte=100),
        only_canonical: Optional[bool] = False
) -> list[EnsemblTranscriptRead]:
    """Get Ensembl transcripts with ensembl_gene_id."""
    get_ensemble_transcripts = select(EnsemblTranscript).where(EnsemblTranscript.ensembl_gene_id == ensembl_gene_id)
    if only_canonical:
        get_ensemble_transcripts = get_ensemble_transcripts.where(EnsemblTranscript.is_canonical)

    get_ensemble_transcripts = session.exec(get_ensemble_transcripts.limit(limit)).all()
    return get_ensemble_transcripts
