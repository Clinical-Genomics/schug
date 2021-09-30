from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .transcript import Transcript, TranscriptRead


class GeneBase(SQLModel):
    chromosome: str
    start: int
    end: int
    hgnc_id: int
    primary_symbol: str


class Gene(GeneBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    transcripts: List["Transcript"] = Relationship(back_populates="gene")


class GeneRead(GeneBase):
    id: int


class GeneReadWithTranscript(GeneRead):
    transcripts: List["TranscriptRead"] = []
