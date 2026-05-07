import pytest
from fastapi import status
from fastapi.testclient import TestClient

from schug.models.common import Build

genome_builds = [Build.build_37, Build.build_38]


@pytest.mark.parametrize("build", genome_builds)
def test_ensembl_genes(
    build,
    client: TestClient,
    endpoints,
    mocker,
):
    """
    Test Ensembl genes streaming endpoint (simplified + stable).
    """

    # -------------------------
    # GIVEN: mocked chromosome stream
    # -------------------------
    async def fake_stream_chromosome(*args, **kwargs):
        yield b"mocked gene line 1\n"
        yield b"mocked gene line 2\n"
        yield b"[success]\n"

    mock_client_instance = mocker.MagicMock()

    mock_client_instance.stream_chromosome = fake_stream_chromosome

    mocker.patch(
        "schug.endpoints.genes.fetch_ensembl_genes",
        return_value=mock_client_instance,
    )

    # -------------------------
    # WHEN: calling endpoint
    # -------------------------
    with client.stream(
        "GET", f"{endpoints.ENSEMBL_GENES.value}?build={build}"
    ) as response:

        # -------------------------
        # THEN: response is OK
        # -------------------------
        assert response.status_code == status.HTTP_200_OK

        lines = [line.strip() for line in response.iter_lines() if line]

        assert len(lines) > 0
        assert "mocked gene line 1" in lines
        assert "mocked gene line 2" in lines
        assert "[success]" in lines
