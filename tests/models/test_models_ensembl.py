from schug.models.ensembl import (
    EnsemblExonRead,
    EnsemblGeneRead,
    EnsemblTranscriptRead
)


def test_into_ensembl_gene_read(
        start_coord,
        end_coord,
        chromosome_entry,
        genome_build_entry
) -> EnsemblGeneRead:
    """Given an instance of EnsemblGene, convert into EnsemblGeneRead"""
    instance = EnsemblGeneRead(
        id=1,
        chromosome=chromosome_entry,
        start=start_coord,
        end=end_coord,
        genome_build=genome_build_entry,
        ensembl_id="ENSG123",
    )

    assert isinstance(instance, EnsemblGeneRead)


def test_into_ensembl_transcript_read(
        start_coord,
        end_coord,
        chromosome_entry,
        genome_build_entry
) -> EnsemblTranscriptRead:
    """Given an instance of EnsemblGene, convert into EnsemblGeneRead"""
    instance = EnsemblTranscriptRead(
        id=1,
        chromosome=chromosome_entry,
        start=start_coord,
        end=end_coord,
        genome_build=genome_build_entry,
        transcript_name="ENST123",
        is_canonical=True,
    )

    assert isinstance(instance, EnsemblTranscriptRead)


def test_into_ensembl_exon_read(
        start_coord,
        end_coord,
        chromosome_entry,
        genome_build_entry
) -> EnsemblExonRead:
    """Given an instance of EnsemblGene, convert into EnsemblGeneRead"""
    instance = EnsemblExonRead(
        id=1,
        chromosome=chromosome_entry,
        start=start_coord,
        end=end_coord,
        genome_build=genome_build_entry,
        ensembl_exon_id="ENSE123",
    )

    assert isinstance(instance, EnsemblExonRead)
