from sqlmodel import SQLModel
from pydantic import validator


class CoordBase(SQLModel):
    chromosome: str
    start: int
    end: int
    genome_build: str

    @validator('genome_build', pre=True)
    def correct_build(cls, v):
        if v != "37" and v != "38":
            raise ValueError(f'genome build: {v} must be either 37 or 38')
        return v
