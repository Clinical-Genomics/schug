from enum import Enum

import pytest
from fastapi.testclient import TestClient
from schug.main import app
from schug.models.gene import Gene


class Endpoints(str, Enum):
    """Contains all the app endpoints used in testing."""

    GENES = "/genes/"


@pytest.fixture(name="simple_client")
def simple_client() -> TestClient:
    """Returns a fastapi.testclient.TestClient used to test the endpoints of an app with an empty database."""
    return TestClient(app)


@pytest.fixture
def endpoints() -> Endpoints:
    """returns an instance of the class Endpoints"""
    return Endpoints


@pytest.fixture(name="schug_gene")
def fixture_gene_id() -> Gene:
    """Return Gene object"""
    return Gene(start=1, end=2, chromosome="1", genome_build="38", ensembl_id="ENSG123")
