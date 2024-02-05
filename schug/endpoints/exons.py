from typing import List

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from schug.load.ensembl import fetch_ensembl_exons
from schug.load.fetch_resource import stream_resource
from schug.models.common import Build

router = APIRouter()


@router.get("/ensembl_exons/", response_class=StreamingResponse)
async def ensembl_exons(build: Build):
    """A proxy to the Ensembl Biomart that retrieves exons in a specific genome build."""

    ensembl_client: EnsemblBiomartClient = fetch_ensembl_exons(build=build)
    url: str = ensembl_client.build_url(xml=ensembl_client.xml)

    return StreamingResponse(stream_resource(url), media_type="text/tsv")
