from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel
from pydantic import Field as PydanticField
from pydantic import validator
from sqlmodel import Field, Relationship, SQLModel


class EnsemblBase(SQLModel):
    ensembl_gene_id: str
    primary_symbol: str
    hgnc_id: int


class Ensembl(EnsemblBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class EnsemblRead(EnsemblBase):
    id: int