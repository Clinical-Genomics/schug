import logging
from typing import Dict, List, Optional

import requests

LOG = logging.getLogger(__name__)
BIOMART_37_URL = "https://feb2014.archive.ensembl.org/biomart/martservice?query="
BIOMART_38_URL = "https://www.ensembl.org/biomart/martservice?query="


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
        }

    @staticmethod
    def create_biomart_xml(filters: dict, attributes: List[str]) -> str:
        """Convert biomart query params into a xml format biomart query"""
        filter_lines: List[str] = EnsemblXML.xml_filters(filters)
        attribute_lines = EnsemblXML.xml_attributes(attributes)
        xml_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            "<!DOCTYPE Query>",
            '<Query  virtualSchemaName = "default" formatter = "TSV" header = "0" uniqueRows'
            ' = "0" count = "" datasetConfigVersion = "0.6" completionStamp = "1">',
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
            formatted_lines.append(f'<Filter name = "{filter_name}" value = "{value}"/>')

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
        self.xml: str = self.xml_creator.create_biomart_xml(filters=filters, attributes=attributes)
        self.header: bool = header

        LOG.info("Setting up ensembl biomart client with server %s", self.server)
        self.query = self._query_service(xml=self.xml)

    def build_url(self, xml: str):
        """Build a query url"""
        return "".join([self.server, xml])

    def _query_service(self, xml: str):
        """Query the Ensembl biomart service and yield the resulting lines
        Accepts:
            xml(str): an xml formatted query, as described here:
                https://grch37.ensembl.org/info/data/biomart/biomart_perl_api.html
            filters(dict): A dictionary w
               attributes(list): A list with attributes to use
            Yields:
                biomartline
        """

        url = self.build_url(xml)
        try:
            with requests.get(url, stream=True) as req:
                for line in req.iter_lines():
                    yield line.decode("utf-8")
        except Exception as ex:
            LOG.info("Error downloading data from biomart: %s", ex)
            raise ex

    def __iter__(self):
        return self

    def __next__(self):
        success = False
        if self.header:
            self.header = False
            return self.xml_creator.create_header(self.attributes)

        line = next(self.query)
        if line.startswith("["):
            if "success" in line:
                success = True
            if not success:
                raise SyntaxError("ensembl request is incomplete")
            raise StopIteration
        if not line:
            raise StopIteration
        return line
