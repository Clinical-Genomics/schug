from typing import List, Optional

from .common import CoordBase

from pydantic import validator
from sqlmodel import Field, Relationship


class EnsemblGeneBase(CoordBase):
    ensembl_id: str

    @validator('ensembl_id', always=True)
    def correct_id(cls, value):
        if not value.startswith("ENSG"):
            raise ValueError(f'{value}: invalid Ensembl gene id')
        return value


class EnsemblGene(EnsemblGeneBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    transcripts: List["EnsemblTranscript"] = Relationship(back_populates="ensembl_gene")


class EnsemblGeneRead(EnsemblGeneBase):
    id: int


class EnsemblGeneCreate(EnsemblGeneBase):
    pass


class EnsemblTranscriptBase(CoordBase):
    transcript_name: str
    is_canonical: bool

    @validator('transcript_name', always=True)
    def correct_id(cls, value):
        if not value.startswith("ENST"):
            raise ValueError(f'{value}: invalid Ensembl transcript id')
        return value


class EnsemblTranscript(EnsemblTranscriptBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    ensembl_gene_id: Optional[int] = Field(foreign_key="ensemblgene.ensembl_id")
    ensembl_gene: Optional["EnsemblGene"] = Relationship(back_populates="transcripts")

    exons: List["EnsemblExon"] = Relationship(back_populates="ensembl_transcript")


class EnsemblTranscriptRead(EnsemblTranscriptBase):
    id: int


class EnsemblExonBase(CoordBase):
    ensembl_exon_id: str

    @validator('ensembl_exon_id', always=True)
    def correct_id(cls, value):
        if not value.startswith("ENSE"):
            raise ValueError(f'{value}: invalid Ensembl exon id')
        return value


class EnsemblExon(EnsemblExonBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    ensembl_transcript_id: Optional[int] = Field(foreign_key="ensembltranscript.transcript_name")
    ensembl_transcript: Optional["EnsemblTranscript"] = Relationship(back_populates="exons")


class EnsemblExonRead(EnsemblExonBase):
    id: int


def into_ensembl_exon_read(exon: EnsemblExon) -> EnsemblExonRead:
    """Explicit definition of Ensembl exon model. Allows flexibility in the external representation of model."""
    return EnsemblExonRead(
        id=exon.id,
        chromosome=exon.chromosome,
        start=exon.start,
        end=exon.end,
        genome_build=exon.genome_build,
        ensembl_exon_id=exon.ensembl_exon_id,
    )


def into_ensembl_gene_read(gene: EnsemblGene) -> EnsemblGeneRead:
    """Explicit definition of Ensembl gene model. Allows flexibility in the external representation of model."""
    return EnsemblGeneRead(
        id=gene.id,
        chromosome=gene.chromosome,
        start=gene.start,
        end=gene.end,
        genome_build=gene.genome_build,
        ensembl_id=gene.ensembl_id,
        transcripts=gene.transcripts,
    )


def into_ensembl_transcript_read(transcript: EnsemblTranscript) -> EnsemblTranscriptRead:
    """Explicit definition of Ensembl transcript model. Allows flexibility in the external representation of model."""
    return EnsemblTranscriptRead(
        id=transcript.id,
        transcript_name=transcript.transcript_name,
        start=transcript.start,
        end=transcript.end,
        chromosome=transcript.chromosome,
        genome_build=transcript.genome_build,
        is_canonical=transcript.is_canonical,
    )
