from schug.database.session import get_session
from schug.models.exon import Exon
from schug.models.gene import Gene
from schug.models.transcript import Transcript
from schug.models.ensembl import EnsemblExon, EnsemblGene, EnsemblTranscript


def load_demo():
    """Load some dummy data into a test instance of schug"""
    with get_session() as session:
        exons = [
            Exon(chromosome="1", start=210111576, end=210111622, exon_name="ENSE00001443254"),
            Exon(chromosome="1", start=210126054, end=210126101, exon_name="ENSE00003523023"),
        ]
        transcripts = [
            Transcript(
                chromosome="1",
                start="1167629",
                end="1170421",
                transcript_name="ENST00000379198",
                refseq_id="NM_080605",
                is_primary=True,
                is_canonical=True,
                exons=exons,
            )
        ]
        genes = [
            Gene(
                chromosome="1",
                start=1167629,
                end=1170421,
                hgnc_id=17978,
                ensembl_id="ENSG00000176022",
                primary_symbol="B3GALT6",
                transcripts=transcripts,
            )
        ]
    for gene in genes:
        session.add(gene)
    session.commit()
    for gene in genes:
        session.refresh(gene)
        print(gene)

    with get_session() as session:
        ensembl_exon = [
            EnsemblExon(
                chromosome="1",
                start=210111576,
                end=210111622,
                genome_build=38,
                ensembl_exon_id="ENSE00001443254",
            )
        ]
        ensembl_transcript = [
            EnsemblTranscript(
                transcript_name="ENST00000379198",
                chromosome="1",
                start="1167629",
                end="1170421",
                is_canonical=True,
                genome_build=38,
                exons=ensembl_exon,
            ),
            EnsemblTranscript(
                transcript_name="ENST00000379198",
                chromosome="1",
                start="1167629",
                end="1170421",
                is_canonical=False,
                genome_build=38,
            )
        ]
        ensembl_gene = [
            EnsemblGene(
                ensembl_id="ENSG00000176022",
                chromosome="1",
                start=1167629,
                end=1170421,
                genome_build=38,
                transcripts=ensembl_transcript
            )
        ]
    for en_gene in ensembl_gene:
        session.add(en_gene)
    session.commit()
    for en_gene in ensembl_gene:
        session.refresh(en_gene)
        print(en_gene)
