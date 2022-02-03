from sqlmodel import SQLModel


class CoordBase(SQLModel):
    chromosome: str
    start: int
    end: int
    genome_build: str
