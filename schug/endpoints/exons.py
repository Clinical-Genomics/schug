from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from schug.load.ensembl import CHROMOSOMES, fetch_ensembl_exons
from schug.models.common import Build

router = APIRouter()

"""
@router.get("/", response_model=List[ExonRead])
def read_exons(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    exons = session.exec(select(Exon).offset(offset).limit(limit)).all()
    return exons
"""


@router.get("/ensembl_exons/", response_class=StreamingResponse)
async def ensembl_exons(
    build: Build,
    max_retries: int = 15,
):
    """ "
    Proxy to Ensembl Biomart that streams exons
    chromosome-by-chromosome with retry support.
    """

    async def chromosome_stream():
        for chrom in CHROMOSOMES:
            print(f"Retrieving chromosome {chrom}")

            client: EnsemblBiomartClient = fetch_ensembl_exons(
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
