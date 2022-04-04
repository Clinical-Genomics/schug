from schug.database.session import get_session

from schug.models.gene import EnsemblGene, Gene, into_gene


def create_gene_item(session: get_session, ensembl_gene: EnsemblGene):
    """Insert Gene Entries"""
    converted = into_gene(ensembl_gene)
    db_entry = Gene.from_orm(converted)
    session.add(db_entry)
    session.commit()
    session.refresh(db_entry)
