from typing import Callable, Type

import pytest
from _io import TextIOWrapper
from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock.plugin import MockerFixture
from requests.models import Response

from schug.demo import TRANSCRIPTS_37_FILE_PATH, TRANSCRIPTS_38_FILE_PATH
from schug.models.common import Build

PROXY_ENDPOINTS_PARAMS = [
    (Build.build_37, TRANSCRIPTS_37_FILE_PATH),
    (Build.build_38, TRANSCRIPTS_38_FILE_PATH),
]


@pytest.mark.parametrize("build, path", PROXY_ENDPOINTS_PARAMS)
def test_ensembl_transcripts_37(
    build: str,
    path: str,
    client: TestClient,
    endpoints: Type,
    mocker: MockerFixture,
    file_handler: Callable,
):
    """Test downloading the transcripts file in both genome builds using the Ensembl Biomart."""

    # GIVEN a patched response from Ensembl Biomart
    tx_lines: TextIOWrapper = file_handler(path)

    async def mock_async_generator(*args, **kwargs):
        for line in tx_lines:
            yield line.encode("utf-8")

    mocker.patch(
        "schug.endpoints.transcripts.stream_resource", side_effect=mock_async_generator
    )

    # WHEN sending a request to Biomart to retrieve transcripts in the given build
    response: Response = client.get(
        f"{endpoints.ENSEMBL_TRANCRIPTS.value}?build={build}"
    )
    # THEN it should return success
    assert response.status_code == status.HTTP_200_OK
    # AND response should contain lines
    assert response.text.rsplit("\n")
