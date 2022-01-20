from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class CoordBase(SQLModel):
    chromosome: str
    start: int
    end: int


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


class EnsemblTranscriptRead(EnsemblTranscriptBase):
    id: int
