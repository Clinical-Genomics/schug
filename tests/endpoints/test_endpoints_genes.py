from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from schug.main import app
from schug.models import GeneRead


client = TestClient(app)


def test_read_genes():
    """Test atlas documents response"""
    # GIVEN a path
    path: str = "/gene"

    # WHEN getting a response
    response = client.get(path)

    # THEN return status ok
    assert response.status_code == 200

    # THEN return schug gene in response
    assert response.json() == [jsonable_encoder(GeneRead)]
