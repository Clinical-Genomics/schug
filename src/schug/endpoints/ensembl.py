from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from schug.database import get_session
from schug.models import EnsemblGene, EnsemblGeneRead
from schug.models import EnsemblTranscript, EnsemblTranscriptRead
from sqlalchemy.exc import NoResultFound
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
):
    ensembl_transcripts = session.exec(select(EnsemblTranscript)
                                       .where(EnsemblTranscript.ensembl_gene_id == ensembl_gene_id)
                                       .limit(limit)).all()
    return ensembl_transcripts


@router.get("/canonical/{ensembl_gene_id}", response_model=EnsemblTranscriptRead)
def read_canonical_ensembl_transcript(
        *,
        ensembl_gene_id: str,
        session: Session = Depends(get_session),
):
    try:
        canonical_transcript = session.exec(select(EnsemblTranscript)
                                            .where(EnsemblTranscript.ensembl_gene_id == ensembl_gene_id)
                                            .where(EnsemblTranscript.is_canonical)).one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gene not found")
    return canonical_transcript
