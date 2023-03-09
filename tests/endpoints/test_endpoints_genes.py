from fastapi import status
from requests.models import Response
from schug.demo import GENES_37_PATH, GENES_38_PATH
from schug.models.common import Build


def test_read_genes_empty_db(client, endpoints):
    """Test read genes response when database is empty."""

    # WHEN getting a response from the genes endpoints of an empty app
    response = client.get(endpoints.GENES)

    # THEN expected status should be 404 (NOT FOUND)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_ensembl_genes_37(client, endpoints, mocker, file_handler):
    """Test downloading the genes file in genome build 37 using the Ensembl Biomart."""

    # GIVEN a patched response from Ensembl Biomart
    gene_lines = file_handler(GENES_37_PATH)
    mocker.patch("schug.endpoints.genes.stream_resource", return_value=gene_lines)

    # WHEN sending a request to Biomart to retrieve genes in build 37
    response: Response = client.get(f"{endpoints.ENSEMBL_GENES}?build={Build.build_37}")
    # THEN it should return success
    assert response.status_code == status.HTTP_200_OK
    # AND response should contain lines
    assert response.text.rsplit("\n")


def test_ensembl_genes_38(client, endpoints, mocker, file_handler):
    """Test downloading the genes file in genome build 38 using the Ensembl Biomart."""

    # GIVEN a patched response from Ensembl Biomart
    gene_lines = file_handler(GENES_38_PATH)
    mocker.patch("schug.endpoints.genes.stream_resource", return_value=gene_lines)

    # WHEN sending a request to Biomart to retrieve genes in build 38
    response: Response = client.get(f"{endpoints.ENSEMBL_GENES}?build={Build.build_38}")
    # THEN it should return success
    assert response.status_code == status.HTTP_200_OK
    # AND response should contain lines
    assert response.text.rsplit("\n")
