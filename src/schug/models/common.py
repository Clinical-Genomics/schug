from typing import Literal

from sqlmodel import SQLModel


class CoordBase(SQLModel):
    chromosome: str
    start: int
    end: int
    genome_build: Literal["37", "38"]
