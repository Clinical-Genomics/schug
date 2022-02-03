from fastapi import FastAPI, status

from .endpoints import exons, genes, transcripts, ensembl

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

app.include_router(
    ensembl.router,
    prefix="/ensembl",
    tags=["ensembl"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)
