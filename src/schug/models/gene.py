from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel
from pydantic import Field as PydanticField
from pydantic import validator
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .transcript import Transcript, TranscriptRead


class GeneBase(SQLModel):
    chromosome: str
    start: int
    end: int
    hgnc_id: int
    primary_symbol: str
    ensembl_id: str


class Gene(GeneBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    transcripts: List["Transcript"] = Relationship(back_populates="gene")


class GeneRead(GeneBase):
    id: int


class GeneReadWithTranscript(GeneRead):
    transcripts: List["TranscriptRead"] = []


class EnsemblGene(BaseModel):
    chromosome: str = PydanticField(..., alias="Chromosome/scaffold name")
    gene_id: str = PydanticField(..., alias="Gene stable ID")
    start: int = PydanticField(..., alias="Gene start (bp)")
    end: int = PydanticField(..., alias="Gene end (bp)")
    hgnc_symbol: Optional[str] = PydanticField(None, alias="HGNC symbol")
    hgnc_id: Optional[int] = PydanticField(None, alias="HGNC ID")

    @validator("*", pre=True)
    def convert_to_none(cls, v):
        if v == "":
            return None
        return v


class HgncGene(BaseModel):
    gene_id: str = PydanticField(..., alias="Gene stable ID")
    ensembl_gene_id: str
    entrez_id: int
    hgnc_symbol: str = PydanticField(None, alias="HGNC symbol")
    hgnc_id: str
    ccds_id: str = None
    short_description: str = PydanticField(None, alias="alias_name")
    alias_symbol: str

    aliases: List[str] = []

    @validator("gene_id", always=True)
    def set_alias_symbols(cls, _, values: dict):
        return values["alias_symbols"].split("|")


"""
{
    "hgnc_id": "HGNC:15766",
    "homeodb": "8666",
    "horde_id": None,
    "imgt": None,
    "intermediate_filament_db": None,
    "iuphar": None,
    "kznf_gene_catalog": None,
    "lncrnadb": None,
    "location": "20q13.13",
    "location_sortable": "20q13.13",
    "locus_group": "protein-coding gene",
    "locus_type": "gene with protein product",
    "lsdb": "",
    "mamit-trnadb": None,
    "merops": None,
    "mgd_id": "MGI:1338758",
    "mirbase": "",
    "name": "activity dependent neuroprotector homeobox",
    "omim_id": "611386",
    "orphanet": "406010",
    "prev_name": "activity-dependent neuroprotector",
    "prev_symbol": "",
    "pseudogene.org": None,
    "pubmed_id": "9872452|11013255",
    "refseq_accession": "NM_181442",
    "rgd_id": "RGD:71030",
    "rna_central_ids": None,
    "snornabase": "",
    "status": "Approved",
    "symbol": "ADNP",
    "ucsc_id": "uc002xvt.3",
    "uniprot_ids": "Q9H2P0",
    "vega_id": "OTTHUMG00000032737",
}
"""
