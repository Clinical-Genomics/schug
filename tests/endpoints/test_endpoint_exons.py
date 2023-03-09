from typing import Callable, Type

from _io import TextIOWrapper
from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock.plugin import MockerFixture
from requests.models import Response
from schug.demo import EXONS_37_PATH, EXONS_38_PATH
from schug.models.common import Build


def test_ensembl_exons_37(
    client: TestClient, endpoints: Type, mocker: MockerFixture, file_handler: Callable
):
    """Test downloading the exons file in genome build 37 using the Ensembl Biomart."""

    # GIVEN a patched response from Ensembl Biomart
    exons_lines: TextIOWrapper = file_handler(EXONS_37_PATH)
    mocker.patch("schug.endpoints.exons.stream_resource", return_value=exons_lines)

    # WHEN sending a request to Biomart to retrieve exons in build 37
    response: Response = client.get(f"{endpoints.ENSEMBL_EXONS}?build={Build.build_37}")
    # THEN it should return success
    assert response.status_code == status.HTTP_200_OK
    # AND response should contain lines
    assert response.text.rsplit("\n")


def test_ensembl_exons_38(
    client: TestClient, endpoints: Type, mocker: MockerFixture, file_handler: Callable
):
    """Test downloading the exons file in genome build 38 using the Ensembl Biomart."""

    # GIVEN a patched response from Ensembl Biomart
    exons_lines: TextIOWrapper = file_handler(EXONS_38_PATH)
    mocker.patch("schug.endpoints.exons.stream_resource", return_value=exons_lines)

    # WHEN sending a request to Biomart to retrieve exons in build 38
    response: Response = client.get(f"{endpoints.ENSEMBL_EXONS}?build={Build.build_38}")
    # THEN it should return success
    assert response.status_code == status.HTTP_200_OK
    # AND response should contain lines
    assert response.text.rsplit("\n")
