from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select

from schug.database.session import get_session
from schug.load.biomart import EnsemblBiomartClient
from schug.load.ensembl import CHROMOSOMES, fetch_ensembl_transcripts
from schug.load.fetch_resource import stream_resource
from schug.models import Transcript, TranscriptRead
from schug.models.common import Build
from schug.models.transcript import TranscriptReadWithExons

router = APIRouter()
"""

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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transcript not found"
        )
    return transcript
"""


@router.get("/ensembl_transcripts/", response_class=StreamingResponse)
async def ensembl_transcripts(
    build: Build,
    max_retries: int = 15,
):
    """
    Proxy to Ensembl Biomart that streams transcripts
    chromosome-by-chromosome with retry support.
    """

    async def chromosome_stream():
        for chrom in CHROMOSOMES:
            print(f"Retrieving chromosome {chrom}")

            client: EnsemblBiomartClient = fetch_ensembl_transcripts(
                build=build,
                chromosomes=[chrom],
            )

            async for chunk in client.stream_chromosome(
                chrom=chrom, max_retries=max_retries
            ):
                yield chunk

    return StreamingResponse(
        chromosome_stream(),
        media_type="text/tsv",
    )
