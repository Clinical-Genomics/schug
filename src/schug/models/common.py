from sqlmodel import SQLModel
from pydantic import validator


class CoordBase(SQLModel):
    chromosome: str
    start: int
    end: int
    genome_build: Literal["37", "38"]
