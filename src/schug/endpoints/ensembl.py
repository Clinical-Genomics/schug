from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from schug.database.ensembl import get_ensembl_exons, get_ensembl_genes, get_ensembl_transcripts
from schug.models import (
    EnsemblExonRead,
    EnsemblGeneRead,
    EnsemblTranscriptRead,
)

router = APIRouter()


@router.get("/", response_model=List[EnsemblGeneRead])
def read_ensembl_genes(
        limit: int = Query(default=100, lte=100),
) -> list[EnsemblGeneRead]:
    """Get all ensembl genes from the database"""
    return get_ensembl_genes(limit)


@router.get("/transcripts/{ensembl_gene_id}", response_model=List[EnsemblTranscriptRead])
def read_ensembl_transcripts(
        ensembl_gene_id: str,
        limit: int = Query(default=100, lte=100),
        only_canonical: Optional[bool] = False
) -> list[EnsemblTranscriptRead]:
    """Get Ensembl transcripts with ensembl gene id."""
    return get_ensembl_transcripts(ensembl_gene_id, only_canonical, limit)


@router.get("/exons/{ensembl_transcript_id}", response_model=List[EnsemblExonRead])
def read_ensembl_exons(
        ensembl_transcript_id: str
) -> list[EnsemblExonRead]:
    """Get Ensembl exons with ensembl transcript id."""
    return get_ensembl_exons(ensembl_transcript_id)
