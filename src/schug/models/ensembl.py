from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .gene import Gene


class EnsemblBase(SQLModel):
    ensembl_id: str = Field(foreign_key="gene.ensembl_id")


class Ensembl(EnsemblBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # define relationship between tables: gene, transcript
    gene: Optional["Gene"] = Relationship(back_populates="ensembl")

class EnsemblCreate():
    pass


class EnsemblRead(EnsemblBase):
    id: int