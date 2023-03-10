from typing import Callable, Type

import pytest
from _io import TextIOWrapper
from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock.plugin import MockerFixture
from requests.models import Response
from schug.demo import GENES_37_FILE_PATH, GENES_38_FILE_PATH
from schug.models.common import Build

PROXY_ENDPOINTS_PARAMS = [
    (Build.build_37, GENES_37_FILE_PATH),
    (Build.build_38, GENES_38_FILE_PATH),
]


def test_read_genes_empty_db(client: TestClient, endpoints: Type):
    """Test read genes response when database is empty."""

    # WHEN getting a response from the genes endpoints of an empty app
    response = client.get(endpoints.GENES)

    # THEN expected status should be 404 (NOT FOUND)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("build, path", PROXY_ENDPOINTS_PARAMS)
def test_ensembl_genes(
    build: str,
    path: str,
    client: TestClient,
    endpoints: Type,
    mocker: MockerFixture,
    file_handler: Callable,
):
    """Test downloading the genes file in both builds using the Ensembl Biomart."""

    # GIVEN a patched response from Ensembl Biomart
    gene_lines: TextIOWrapper = file_handler(path)
    mocker.patch("schug.endpoints.genes.stream_resource", return_value=gene_lines)

    # WHEN sending a request to Biomart to retrieve genes in the given build
    response: Response = client.get(f"{endpoints.ENSEMBL_GENES}?build={build}")
    # THEN it should return success
    assert response.status_code == status.HTTP_200_OK
    # AND response should contain lines
    assert response.text.rsplit("\n")
