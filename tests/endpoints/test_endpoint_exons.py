import asyncio
import io
from typing import Callable, Type

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock.plugin import MockerFixture

from schug.demo import EXONS_37_FILE_PATH, EXONS_38_FILE_PATH
from schug.models.common import Build

genome_builds = [Build.build_37, Build.build_38]


@pytest.mark.parametrize("build", genome_builds)
def test_ensembl_exons(
    build: str,
    client: TestClient,
    endpoints: Type,
    mocker: MockerFixture,
    file_handler: Callable,
):
    """Test downloading the exons file in both builds using the Ensembl Biomart."""

    # GIVEN a patched response from Ensembl Biomart
    mock_ensembl_client = mocker.MagicMock()
    mock_ensembl_client.build_url.return_value = "https://mocked_url"

    mocker.patch(
        "schug.endpoints.exons.fetch_ensembl_exons", return_value=mock_ensembl_client
    )

    # Properly mock urlopen
    mock_urlopen = mocker.patch("urllib.request.urlopen")
    mock_urlopen.return_value.__enter__.return_value = io.BytesIO(
        b"mocked exon line 1\nmocked exon line 2\n[success]\n"
    )
    # GIVEN a mocked interval between requests to Biomart
    mocker.patch("asyncio.sleep")

    # WHEN sending a request to Biomart to retrieve exons in the given build
    with client.stream(
        "GET", f"{endpoints.ENSEMBL_EXONS.value}?build={build}"
    ) as response:
        assert response.status_code == status.HTTP_200_OK

        # THEN response should contain lines
        lines = [
            line.strip() for line in response.iter_lines()
        ]  # Strip newline characters
        assert len(lines) > 0
        assert "mocked exon line 1" in lines
        assert "mocked exon line 2" in lines
        assert "[success]" in lines
