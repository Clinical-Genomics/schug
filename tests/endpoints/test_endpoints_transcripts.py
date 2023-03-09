from fastapi import status
from requests.models import Response
from schug.demo import TRANSCRIPTS_37_PATH, TRANSCRIPTS_38_PATH
from schug.models.common import Build


def test_ensembl_transcripts_37(client, endpoints, mocker, file_handler):
    """Test downloading the transcripts file in genome build 37 using the Ensembl Biomart."""

    # GIVEN a patched response from Ensembl Biomart
    tx_lines = file_handler(TRANSCRIPTS_37_PATH)
    mocker.patch("schug.endpoints.transcripts.stream_resource", return_value=tx_lines)

    # WHEN sending a request to Biomart to retrieve transcripts in build 37
    response: Response = client.get(f"{endpoints.ENSEMBL_TRANCRIPTS}?build={Build.build_37}")
    # THEN it should return success
    assert response.status_code == status.HTTP_200_OK
    # AND response should contain lines
    assert response.text.rsplit("\n")


def test_ensembl_transcripts_38(client, endpoints, mocker, file_handler):
    """Test downloading the transcripts file in genome build 38 using the Ensembl Biomart."""

    # GIVEN a patched response from Ensembl Biomart
    tx_lines = file_handler(TRANSCRIPTS_38_PATH)
    mocker.patch("schug.endpoints.transcripts.stream_resource", return_value=tx_lines)

    # WHEN sending a request to Biomart to retrieve transcripts in build 38
    response: Response = client.get(f"{endpoints.ENSEMBL_TRANCRIPTS}?build={Build.build_38}")
    # THEN it should return success
    assert response.status_code == status.HTTP_200_OK
    # AND response should contain lines
    assert response.text.rsplit("\n")
