import pytest

from schug.models.gene import Gene


@pytest.fixture(name="schug_gene")
def fixture_gene_id() -> Gene:
    """Return Gene object"""
    return Gene(
        start=1,
        end=2,
        chromosome="1",
        genome_build="38",
        ensembl_id="ENSG123"
    )
