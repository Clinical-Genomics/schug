from enum import Enum
from typing import Literal

from pydantic import validator
from sqlmodel import SQLModel


class Build(str, Enum):
    build_37 = "37"
    build_38 = "38"


class CoordBase(SQLModel):
    chromosome: str
    start: int
    end: int
    resource: str
    resource_id: str
    genome_build: str

    @validator("genome_build", pre=True)
    def correct_build(cls, v):
        if v != "37" and v != "38":
            raise ValueError(f"genome build: {v} must be either 37 or 38")
        return v