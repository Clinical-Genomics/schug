from typing import Callable, Type

import pytest
from _io import TextIOWrapper
from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock.plugin import MockerFixture
from requests.models import Response
from schug.demo import EXONS_37_PATH, EXONS_38_PATH
from schug.models.common import Build

PROXY_ENDPOINTS_PARAMS = [(Build.build_37, EXONS_37_PATH), (Build.build_38, EXONS_38_PATH)]


@pytest.mark.parametrize("build, path", PROXY_ENDPOINTS_PARAMS)
def test_ensembl_exons(
    build: str,
    path: str,
    client: TestClient,
    endpoints: Type,
    mocker: MockerFixture,
    file_handler: Callable,
):
    """Test downloading the exons file in both builds using the Ensembl Biomart."""
    # GIVEN a patched response from Ensembl Biomart
    exons_lines: TextIOWrapper = file_handler(path)
    mocker.patch("schug.endpoints.exons.stream_resource", return_value=exons_lines)

    # WHEN sending a request to Biomart to retrieve exons in the given build
    response: Response = client.get(f"{endpoints.ENSEMBL_EXONS}?build={build}")
    # THEN it should return success
    assert response.status_code == status.HTTP_200_OK
    # AND response should contain lines
    assert response.text.rsplit("\n")
