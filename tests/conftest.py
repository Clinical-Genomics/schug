from enum import Enum

import pytest
from _io import TextIOWrapper
from fastapi.testclient import TestClient
from schug.main import app


class Endpoints(str, Enum):
    """Contains all the app endpoints used in testing."""

    GENES = "/genes/"
    ENSEMBL_GENES = "/genes/ensembl_genes/"
    ENSEMBL_TRANCRIPTS = "/transcripts/ensembl_transcripts/"
    ENSEMBL_EXONS = "/exons/ensembl_exons/"


@pytest.fixture(name="client")
def client() -> TestClient:
    """Returns a fastapi.testclient.TestClient used to test the endpoints of an app with an empty database."""

    return TestClient(app)


@pytest.fixture
def endpoints() -> Endpoints:
    """Returns an instance of the class Endpoints."""
    return Endpoints


@pytest.fixture(name="file_handler")
def file_handler() -> TextIOWrapper:
    """Get a file handler to a resource file."""

    def _open_file(file_path: str) -> TextIOWrapper:
        return open(file_path, "r", encoding="utf-8")

    return _open_file
