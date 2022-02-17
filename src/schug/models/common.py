from sqlmodel import SQLModel
from pydantic import validator


class CoordBase(SQLModel):
    chromosome: str
    start: int
    end: int
    genome_build: int

    @validator('genome_build', always=True)
    def correct_build(cls, value):
        if value != 37 and value != 38:
            raise ValueError(f'genome build: {value} must be either 37 or 38')
        return value
