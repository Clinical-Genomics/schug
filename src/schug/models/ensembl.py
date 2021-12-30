from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel
from pydantic import Field as PydanticField
from pydantic import validator
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .gene import GeneBase, EnsemblGene


class Ensembl(GeneBase, table=True):
    pass


class EnsemblCreate():
    pass


class EnsemblRead():
    id: int