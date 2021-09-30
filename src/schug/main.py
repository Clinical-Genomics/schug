from typing import List

from fastapi import Depends, FastAPI, Query, status
from sqlmodel import Session, select

from .database import create_db_and_tables, get_session
from .endpoints import genes
from .models import Exon, ExonRead, Transcript, TranscriptRead

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to Schug: the magic gene, transcript and exon database"}


app.include_router(
    genes.router,
    prefix="/genes",
    tags=["genes"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@app.get("/exons/", response_model=List[ExonRead])
def read_exons(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    exons = session.exec(select(Exon).offset(offset).limit(limit)).all()
    return exons


@app.get("/transcripts/", response_model=List[TranscriptRead])
def read_transcripts(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    transcripts = session.exec(select(Transcript).offset(offset).limit(limit)).all()
    return transcripts


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
