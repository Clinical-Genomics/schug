from fastapi import FastAPI, status

from .database import create_db_and_tables
from .endpoints import exons, genes, transcripts

app = FastAPI()

### REST API


@app.get("/")
async def root():
    return {"message": "Welcome to Schug: the magic gene, transcript and exon database"}


app.include_router(
    genes.router,
    prefix="/genes",
    tags=["genes"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


app.include_router(
    transcripts.router,
    prefix="/transcripts",
    tags=["transcripts"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

app.include_router(
    exons.router,
    prefix="/exons",
    tags=["exons"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
