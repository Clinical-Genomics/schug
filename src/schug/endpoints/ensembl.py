from typing import List, Optional

from fastapi import APIRouter, Query
from .http_exceptions import SchugHttpException
from schug.database.ensembl import (
    get_ensembl_exons, put_ensembl_gene,
    get_ensembl_genes,
    get_ensembl_transcripts
)
from schug.models import (
    EnsemblGene, EnsemblExonRead,
    EnsemblGeneCreate,
    EnsemblGeneRead,
    EnsemblTranscriptRead,
)

router = APIRouter()


@router.get("/", response_model=List[EnsemblGeneRead])
def read_ensembl_genes(
        *,
        limit: int = Query(default=100, lte=100),
) -> list[EnsemblGeneRead]:
    """Get all ensembl genes from the database"""
    genes: List[EnsemblGeneRead] = get_ensembl_genes(limit)
    SchugHttpException.error_404(result=genes, query="Ensembl Genes")
    return genes


@router.post("/", response_model=EnsemblGene)
def create_ensembl_gene(*, gene: EnsemblGeneCreate) -> EnsemblGene:
    """Put a record of Ensembl gene into the db."""
    return put_ensembl_gene(gene)


@router.get("/transcripts/{ensembl_gene_id}", response_model=List[EnsemblTranscriptRead])
def read_ensembl_transcripts(
        *,
        ensembl_gene_id: str,
        limit: int = Query(default=100, lte=100),
        only_canonical: Optional[bool] = False
) -> list[EnsemblTranscriptRead]:
    """Get Ensembl transcripts with ensembl gene id."""
    result: List[EnsemblTranscriptRead] = get_ensembl_transcripts(ensembl_gene_id, only_canonical, limit)
    SchugHttpException.error_404(result=result, query=ensembl_gene_id)
    return result


@router.get("/exons/{ensembl_transcript_id}", response_model=List[EnsemblExonRead])
def read_ensembl_exons(
        *,
        ensembl_transcript_id: str
) -> list[EnsemblExonRead]:
    """Get Ensembl exons with ensembl transcript id."""
    result: List[EnsemblExonRead] = get_ensembl_exons(ensembl_transcript_id)
    SchugHttpException.error_404(result=result, query=ensembl_transcript_id)
    return result
