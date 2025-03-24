from enum import Enum

import pytest
from _io import TextIOWrapper
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from schug.database.session import get_session
from schug.main import app
from schug.models.common import Build
from schug.models.gene import Gene

TEST_DB = "sqlite:///./test.db"
DEMO_CONNECT_ARGS = {"check_same_thread": False}

engine = create_engine(TEST_DB, connect_args=DEMO_CONNECT_ARGS)


class Endpoints(str, Enum):
    """Contains all the app endpoints used in testing."""

    GENES = "/genes/"
    ENSEMBL_GENES = "/genes/ensembl_genes/"
    ENSEMBL_TRANSCRIPTS = "/transcripts/ensembl_transcripts/"
    ENSEMBL_EXONS = "/exons/ensembl_exons/"


@pytest.fixture(name="session")
def session_fixture() -> Session:
    """Returns an object of type sqlalchemy.orm.session.sessionmaker."""

    SQLModel.metadata.create_all(engine)

    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(name="client")
def client(session) -> TestClient:
    """Returns a fastapi.testclient.TestClient used to test the endpoints of an app with an empty database."""

    def _override_get_db():
        try:
            db = session
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_session] = _override_get_db

    return TestClient(app)


@pytest.fixture
def endpoints() -> Endpoints:
    """Returns an instance of the class Endpoints."""
    return Endpoints


@pytest.fixture(name="schug_gene")
def fixture_gene_id() -> Gene:
    """Return a Gene object."""
    return Gene(
        start=1,
        end=2,
        chromosome="1",
        genome_build=Build.build_38,
        ensembl_id="ENSG123",
    )


@pytest.fixture(name="file_handler")
def file_handler() -> TextIOWrapper:
    """Get a file handler to a resource file."""

    def _open_file(file_path: str) -> TextIOWrapper:
        return open(file_path, "r", encoding="utf-8")

    return _open_file
