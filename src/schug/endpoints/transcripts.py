from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import FileResponse
from schug.database.session import get_session
from schug.models import Transcript, TranscriptRead
from schug.models.transcript import TranscriptReadWithExons
from sqlmodel import Session, select

router = APIRouter()


@router.get("/", response_model=List[TranscriptRead])
def read_transcripts(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    transcripts = session.exec(select(Transcript).offset(offset).limit(limit)).all()
    return transcripts


@router.get("/{db_id}", response_model=TranscriptReadWithExons)
def read_transcript_db_id(
    *,
    db_id: int,
    session: Session = Depends(get_session),
):
    transcript = session.get(Transcript, db_id)
    if not transcript:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transcript not found")
    return transcript


@router.get("/ensembl_transcripts/{build}", response_class=FileResponse)
def ensembl_transcripts():
    """A proxy endpooint to the Ensembl transcripts in the given genome build"""
