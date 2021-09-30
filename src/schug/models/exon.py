from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel
from src.schug.models.link_tables import ExonTranscriptLink

if TYPE_CHECKING:
    from .transcript import Transcript


class ExonBase(SQLModel):
    chromosome: str
    start: int
    end: int
    exon_name: Optional[str]


class Exon(ExonBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    transcripts: List["Transcript"] = Relationship(
        back_populates="exons", link_model=ExonTranscriptLink
    )


class ExonRead(ExonBase):
    id: int
