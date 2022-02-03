from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from schug.database.session import get_session
from schug.models import Exon, ExonRead
from sqlmodel import Session, select

router = APIRouter()


@router.get("/", response_model=List[ExonRead])
def read_exons(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    exons = session.exec(select(Exon).offset(offset).limit(limit)).all()
    return exons
