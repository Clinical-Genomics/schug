import csv
import logging
from typing import List, Optional

from pydantic import parse_obj_as
from schug.load.biomart import EnsemblBiomartClient
from schug.models.exon import EnsemblExon

LOG = logging.getLogger(__name__)

AUTOSOMES = [str(nr) for nr in range(1, 23)]
CHROMOSOMES = AUTOSOMES + [
    "X",
    "Y",
    "MT",
]
CHROMOSOMES_38 = AUTOSOMES + ["X", "Y", "M"]


def fetch_ensembl_biomart(attributes: List[str], filters: dict, build=None) -> EnsemblBiomartClient:
    """Fetch data from ensembl biomart
    Args:
        attributes(list): List of selected attributes
        filters(dict): Select what filters to use
        build(str): '37' or '38'
    Returns:
        client(EnsemblBiomartClient)
    """
    build = build or "37"

    client = EnsemblBiomartClient(build=build, filters=filters, attributes=attributes)
    LOG.info("Selecting attributes: %s", ", ".join(attributes))
    LOG.info("Use filter: %s", filters)

    return client


def fetch_ensembl_genes(build: str, chromosomes: List[str] = None) -> EnsemblBiomartClient:
    """Fetch genes from ensembl"""
    chromosomes: List[str] = chromosomes or CHROMOSOMES
    LOG.info("Fetching ensembl genes")

    attributes = [
        "chromosome_name",
        "start_position",
        "end_position",
        "ensembl_gene_id",
        "hgnc_symbol",
        "hgnc_id",
    ]

    filters = {"chromosome_name": chromosomes}

    return fetch_ensembl_biomart(attributes=attributes, filters=filters, build=build)


def fetch_ensembl_transcripts(
    build: str, chromosomes: Optional[List[str]] = None
) -> EnsemblBiomartClient:
    """Fetch the ensembl transcripts"""
    chromosomes = chromosomes or CHROMOSOMES
    LOG.info("Fetching ensembl transcripts")

    attributes = [
        "chromosome_name",
        "ensembl_gene_id",
        "ensembl_transcript_id",
        "transcript_start",
        "transcript_end",
        "refseq_mrna",
        "refseq_mrna_predicted",
        "refseq_ncrna",
        "transcript_mane_select",
        "transcript_mane_plus_clinical",
    ]

    filters = {"chromosome_name": chromosomes}

    return fetch_ensembl_biomart(attributes=attributes, filters=filters, build=build)


def fetch_ensembl_exon_lines(
    build: str, chromosomes: Optional[List[str]] = None
) -> EnsemblBiomartClient:
    """Fetch the ensembl exons"""
    chromosomes = chromosomes or CHROMOSOMES
    LOG.info("Fetching ensembl exons")

    attributes = [
        "chromosome_name",
        "ensembl_gene_id",
        "ensembl_transcript_id",
        "ensembl_exon_id",
        "exon_chrom_start",
        "exon_chrom_end",
        "5_utr_start",
        "5_utr_end",
        "3_utr_start",
        "3_utr_end",
        "strand",
        "rank",
    ]

    filters = {"chromosome_name": chromosomes}

    return fetch_ensembl_biomart(attributes=attributes, filters=filters, build=build)


def fetch_ensembl_exons(build: str, chromosomes: Optional[List[str]] = None) -> List[EnsemblExon]:
    """Fetch ensembl exon objects"""
    exon_lines: EnsemblBiomartClient = fetch_ensembl_exon_lines(
        build=build, chromosomes=chromosomes
    )

    parsed_exons = parse_obj_as(
        List[EnsemblExon], [exon_info for exon_info in csv.DictReader(exon_lines, delimiter="\t")]
    )
    return parsed_exons
