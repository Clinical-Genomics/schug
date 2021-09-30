from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from .link_tables import ExonTranscriptLink

if TYPE_CHECKING:
    from .exon import Exon
    from .gene import Gene


class TranscriptBase(SQLModel):
    chromosome: str
    start: int
    end: int
    transcript_name: str
    is_primary: bool = False
    is_canonical: bool = False

    gene_id: Optional[int] = Field(default=None, foreign_key="gene.id")


class Transcript(TranscriptBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    gene: Optional["Gene"] = Relationship(back_populates="transcripts")
    exons: List["Exon"] = Relationship(back_populates="transcripts", link_model=ExonTranscriptLink)


class TranscriptRead(TranscriptBase):
    id: int
