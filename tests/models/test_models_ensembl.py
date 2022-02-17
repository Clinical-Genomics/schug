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
    return EnsemblGeneRead(
        id=1,
        chromosome=chromosome_entry,
        start=start_coord,
        end=end_coord,
        genome_build=genome_build_entry,
        ensembl_id="ENSG123",
    )


def test_into_ensembl_transcript_read(
        start_coord,
        end_coord,
        chromosome_entry,
        genome_build_entry
) -> EnsemblTranscriptRead:
    """Given an instance of EnsemblGene, convert into EnsemblGeneRead"""
    return EnsemblTranscriptRead(
        id=1,
        chromosome=chromosome_entry,
        start=start_coord,
        end=end_coord,
        genome_build=genome_build_entry,
        transcript_name="ENST123",
        is_canonical=True,
    )


def test_into_ensembl_exon_read(
        start_coord,
        end_coord,
        chromosome_entry,
        genome_build_entry
) -> EnsemblExonRead:
    """Given an instance of EnsemblGene, convert into EnsemblGeneRead"""
    return EnsemblExonRead(
        id=1,
        chromosome=chromosome_entry,
        start=start_coord,
        end=end_coord,
        genome_build=genome_build_entry,
        ensembl_exon_id="ENSE123",
    )


