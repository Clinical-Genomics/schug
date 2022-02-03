from sqlmodel import select

from schug.database.session import get_session
from schug.models import EnsemblTranscript, into_ensembl_transcript
from schug.models import EnsemblGene


def get_ensembl_genes(limit=100):
    query = select(EnsemblGene)

    with get_session() as session:
        queried_genes = session.exec(query.limit(limit)).all()

        return queried_genes


def get_ensembl_transcripts(ensembl_gene_id, only_canonical, limit=100):
    query = select(EnsemblTranscript).where(EnsemblTranscript.ensembl_gene_id == ensembl_gene_id)
    if only_canonical:
        query = query.where(EnsemblTranscript.is_canonical)

    with get_session() as session:
        queried_transcripts = session.exec(query.limit(limit)).all()

        ensembl_transcripts = []
        for t in queried_transcripts:
            ensembl_transcripts.append(into_ensembl_transcript(t))

        return ensembl_transcripts


def update_ensembl(gene):
    """Update the ensemblgene table"""
    pass
