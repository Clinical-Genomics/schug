from fastapi import status
from fastapi.testclient import TestClient
from schug import __version__


def test_root(client: TestClient):
    """Test the root endpoint."""
    # WHEN user makes a call to the root endpoint
    response = client.get("/")
    # THEN it should return success
    assert response.status_code == status.HTTP_200_OK
    # AND the expected message
    assert response.json() == {"message": f"Welcome to Schug v.{__version__}!"}
