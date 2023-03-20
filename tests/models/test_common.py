from schug.models.common import Build


def test_build():
    """Test accepted valued for Build class."""
    for item in ["37", "38", "GRCh37", "GRCh38"]:
        assert type(Build(item)) == Build
        assert Build(item)
