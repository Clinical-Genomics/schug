from typing import List

from fastapi import APIRouter, Depends, Query
from schug.database import get_session
from schug.models import Ensembl, EnsemblRead
from sqlmodel import Session, select

router = APIRouter()


@router.get("/", response_model=List[EnsemblRead])
def read_ensembl_genes(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    ensembl_genes = session.exec(select(Ensembl).offset(offset).limit(limit)).all()
    return ensembl_genes