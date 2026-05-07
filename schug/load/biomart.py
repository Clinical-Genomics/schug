import asyncio
import logging
import random
import urllib
from typing import Dict, List, Optional
from urllib.error import URLError

import requests

LOG = logging.getLogger(__name__)
BIOMART_37_URL = "https://grch37.ensembl.org/biomart/martservice/?query="
BIOMART_38_URL = "https://www.ensembl.org/biomart/martservice/?query="


class EnsemblOutageError(Exception):
    """Raised when Ensembl returns an HTML outage page instead of data."""

    pass


class EnsemblXML:
    """Class with functions to create xml query files for ensembl biomart

    A conversion table is used to ensure that the output format is the same as the one fetched from ensembl biomart
    """

    def __init__(self):
        self.attribute_to_header = {
            "chromosome_name": "Chromosome/scaffold name",
            "ensembl_gene_id": "Gene stable ID",
            "ensembl_transcript_id": "Transcript stable ID",
            "ensembl_exon_id": "Exon stable ID",
            "exon_chrom_start": "Exon region start (bp)",
            "exon_chrom_end": "Exon region end (bp)",
            "5_utr_start": "5' UTR start",
            "5_utr_end": "5' UTR end",
            "3_utr_start": "3' UTR start",
            "3_utr_end": "3' UTR end",
            "strand": "Strand",
            "rank": "Exon rank in transcript",
            "transcript_start": "Transcript start (bp)",
            "transcript_end": "Transcript end (bp)",
            "refseq_mrna": "RefSeq mRNA ID",
            "refseq_mrna_predicted": "RefSeq mRNA predicted ID",
            "refseq_ncrna": "RefSeq ncRNA ID",
            "start_position": "Gene start (bp)",
            "end_position": "Gene end (bp)",
            "hgnc_symbol": "HGNC symbol",
            "hgnc_id": "HGNC ID",
            "gene_biotype": "Gene Biotype",
        }

    @staticmethod
    def create_biomart_xml(
        filters: dict, attributes: List[str], header: Optional[bool]
    ) -> str:
        """Convert Ensembl Biomart query parameters into a XML format Ensembl Biomart query."""
        filter_lines: List[str] = EnsemblXML.xml_filters(filters)
        attribute_lines = EnsemblXML.xml_attributes(attributes)
        xml_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            "<!DOCTYPE Query>",
            f'<Query  virtualSchemaName = "default" formatter = "TSV" header = "{0 if header is False else 1}" uniqueRows'
            ' = "1" count = "0" datasetConfigVersion = "0.6" completionStamp = "1">',
            "",
            '\t<Dataset name = "hsapiens_gene_ensembl" interface = "default" >',
        ]
        for line in filter_lines:
            xml_lines.append("\t\t" + line)
        for line in attribute_lines:
            xml_lines.append("\t\t" + line)
        xml_lines += ["\t</Dataset>", "</Query>"]

        return "".join(xml_lines)

    @staticmethod
    def xml_filters(filters: dict) -> List[str]:
        """Creates a filter line for the biomart xml document"""

        formatted_lines = []
        for filter_name in filters:
            value = filters[filter_name]
            if not isinstance(value, str):
                value = ",".join(value)
            formatted_lines.append(
                f'<Filter name = "{filter_name}" value = "{value}"/>'
            )

        return formatted_lines

    @staticmethod
    def xml_attributes(attributes: List[str]) -> List[str]:
        """Creates an attribute line for the biomart xml document"""
        return [f'<Attribute name = "{attr}" />' for attr in attributes]

    def create_header(self, attributes: List[str]) -> str:
        """Create a header line based on the attributes
        Args:
            attributes(list(str))
        Returns:
            header(str)
        """
        headers = [self.attribute_to_header[attr] for attr in attributes]

        return "\t".join(headers)


class EnsemblBiomartClient:
    """Class to handle requests to the ensembl biomart api"""

    def __init__(
        self,
        build: str = "37",
        filters: Optional[dict] = None,
        attributes: List[str] = None,
        header: bool = True,
    ):
        """Initialise a ensembl biomart client"""
        self.xml_creator = EnsemblXML()
        self.server = BIOMART_37_URL
        if build == "38":
            self.server = BIOMART_38_URL
        self.filters: dict = filters or {}
        self.attributes: List[str] = attributes or []
        self.header: bool = header
        self.xml: str = self.xml_creator.create_biomart_xml(
            filters=filters, attributes=attributes, header=header
        )

        LOG.info("Setting up ensembl biomart client with server %s", self.server)

    def build_url(self, xml: str):
        """Build a query url"""
        return "".join([self.server, xml])

    async def stream_chromosome(self, chrom: str, max_retries: int):
        """Stream content of response by chromosome, taking care of eventual server errors."""

        url = self.build_url(xml=self.xml)

        encoded_url = urllib.parse.quote(
            url,
            safe=":/?=&",
        )

        delay = 1

        for attempt in range(1, max_retries + 1):
            try:
                print(f"[{chrom}] Attempt {attempt}")

                with urllib.request.urlopen(
                    encoded_url,
                    timeout=60,
                ) as response:

                    # Detect Ensembl outage HTML pages
                    first_chunk = response.read(1000)

                    if b"<html" in first_chunk.lower():
                        raise EnsemblOutageError("Ensembl returned outage page")

                    # Yield first chunk
                    yield first_chunk

                    # Stream remaining data
                    for line in response:
                        yield line

                    # Success → stop retrying
                    return

            except (URLError, EnsemblOutageError) as e:
                print(f"[{chrom}] Error: {e}")

                if attempt == max_retries:
                    print(f"[{chrom}] Failed after {max_retries} attempts")
                    return

                await asyncio.sleep(delay + random.uniform(0, 0.5))

                delay *= 2
