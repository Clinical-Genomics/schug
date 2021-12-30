from typing import Optional

from sqlmodel import Field
from .exon import EnsemblExon
from .gene import GeneBase, EnsemblGene
from .transcript import EnsemblTranscript


class EnsemblBase(GeneBase):
    pass


class Ensembl(EnsemblBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class EnsemblCreate():
    pass


class EnsemblRead(EnsemblBase):
    id: int