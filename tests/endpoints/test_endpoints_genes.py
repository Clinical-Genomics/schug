from fastapi import status
from fastapi.encoders import jsonable_encoder
from schug.models import GeneRead


def test_read_genes_empty_db(client, endpoints):
    """Test read genes response when database is empty"""

    # WHEN getting a response from the genes endpoints of an empty app
    response = client.get(endpoints.GENES)

    # THEN expected status should be 404 (NOT FOUND)
    assert response.status_code == status.HTTP_404_NOT_FOUND
