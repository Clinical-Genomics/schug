from typing import List, Optional

from .common import CoordBase
from sqlmodel import Field, Relationship


class EnsemblGeneBase(CoordBase):
    ensembl_id: str


class EnsemblGene(EnsemblGeneBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    transcripts: List["EnsemblTranscript"] = Relationship(back_populates="ensembl_gene")


class EnsemblGeneRead(EnsemblGeneBase):
    id: int


class EnsemblTranscriptBase(CoordBase):
    transcript_name: str
    is_canonical: bool


class EnsemblTranscript(EnsemblTranscriptBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    ensembl_gene_id: Optional[int] = Field(foreign_key="ensemblgene.ensembl_id")
    ensembl_gene: Optional["EnsemblGene"] = Relationship(back_populates="transcripts")

    exons: List["EnsemblExon"] = Relationship(back_populates="ensembl_transcript")


class EnsemblTranscriptRead(EnsemblTranscriptBase):
    id: int


class EnsemblExonBase(CoordBase):
    ensembl_exon_id: str


class EnsemblExon(EnsemblExonBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    ensembl_transcript_id: Optional[int] = Field(foreign_key="ensembltranscript.transcript_name")
    ensembl_transcript: Optional["EnsemblTranscript"] = Relationship(back_populates="exons")


class EnsemblExonRead(EnsemblExonBase):
    id: int


def into_ensembl_transcript(ensembl_transcript: EnsemblTranscript) -> EnsemblTranscriptRead:
    """Explicit definition of Ensembl transcript model, allows one -> many relationships in one model."""
    return EnsemblTranscriptRead(
        id=ensembl_transcript.id,
        transcript_name=ensembl_transcript.transcript_name,
        start=ensembl_transcript.start,
        end=ensembl_transcript.end,
        chromosome=ensembl_transcript.chromosome,
        genome_build=ensembl_transcript.genome_build,
        is_canonical=ensembl_transcript.is_canonical,
    )
