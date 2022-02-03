from typing import List

from sqlmodel import select

from schug.database.session import get_session
from schug.models import (
    EnsemblExon, EnsemblExonRead, into_ensembl_exon_read,
    EnsemblGene, EnsemblGeneRead, into_ensembl_gene_read,
    EnsemblTranscript, EnsemblTranscriptRead, into_ensembl_transcript_read,
)


def get_ensembl_genes(limit: int = 100) -> List["EnsemblGeneRead"]:
    """Get a limited collection of Ensembl genes."""
    query = select(EnsemblGene)

    with get_session() as session:
        queried_genes = session.exec(query.limit(limit)).all()

        converted = []
        for item in queried_genes:
            converted.append(into_ensembl_gene_read(item))

        return converted


def get_ensembl_transcripts(
        gene_id: str, only_canonical: bool, limit: int = 100
) -> List[EnsemblTranscriptRead]:
    """Get a limited collection of Ensembl transcripts with gene ID and a filter for canonical."""
    query = select(EnsemblTranscript).where(EnsemblTranscript.ensembl_gene_id == gene_id)
    if only_canonical:
        query = query.where(EnsemblTranscript.is_canonical)

    with get_session() as session:
        queried_transcripts = session.exec(query.limit(limit)).all()

        converted = []
        for item in queried_transcripts:
            converted.append(into_ensembl_transcript_read(item))

        return converted


def get_ensembl_exons(transcript_id: str) -> List[EnsemblExonRead]:
    """Get a collection of Ensembl exons with transcript ID."""
    query = select(EnsemblExon).where(EnsemblExon.ensembl_transcript_id == transcript_id)

    with get_session() as session:
        queried_exons = session.exec(query).all()

        converted = []
        for item in queried_exons:
            converted.append(into_ensembl_exon_read(item))

        return queried_exons


def update_ensembl(gene):
    """Update the ensemblgene table"""
    pass
