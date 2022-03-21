import pytest

from fastapi import HTTPException

from schug.endpoints.http_exceptions import SchugHttpException
from schug.models.gene import Gene


def test_gene_id_http_exception_error_404_when_found(schug_gene: Gene):
    """Test raise 404 when found"""
    # GIVEN a gene id

    # WHEN id for gene is found
    raised_error = SchugHttpException.error_404(result=schug_gene, query=schug_gene.id)

    # THEN HTTPError should not be raised
    assert raised_error is None


def test_gene_http_exception_error_404(schug_gene: Gene):
    """Test raise 404 when not found"""
    # GIVEN a gene id

    # WHEN id for gene is not found
    with pytest.raises(HTTPException):
        # THEN raise HTTPException
        SchugHttpException.error_404(result=False, query=schug_gene.id)
