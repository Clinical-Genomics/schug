from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from schug.database.ensembl import get_ensembl_genes, get_ensembl_transcripts
from schug.models import EnsemblGeneRead
from schug.models import EnsemblTranscriptRead

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
    """Get Ensembl transcripts with ensembl_gene_id."""
    return get_ensembl_transcripts(ensembl_gene_id, only_canonical, limit)
