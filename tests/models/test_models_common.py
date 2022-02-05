from schug.models.common import CoordBase


def test_coordbase_genome_build(start_coord, end_coord, chromosome_entry, genome_build_entry):
    # Given an instance of CoordBase
    instance = CoordBase(
        chromosome=chromosome_entry,
        start=start_coord,
        end=end_coord,
        genome_build=genome_build_entry,
    )

    assert isinstance(instance, CoordBase)
