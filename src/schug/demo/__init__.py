import pkg_resources

# Filenames
EXONS_37: str = "demo/exons_37.tsv"
EXONS_38: str = "demo/exons_38.tsv"
GENES_37: str = "demo/genes_37.tsv"
GENES_38: str = "demo/genes_38.tsv"
TRANCRIPTS_37: str = "demo/transcripts_37.tsv"
TRANCRIPTS_38: str = "demo/transcripts_38.tsv"

# Paths
EXONS_37_PATH: str = pkg_resources.resource_filename("schug", EXONS_37)
EXONS_38_PATH: str = pkg_resources.resource_filename("schug", EXONS_38)
GENES_37_PATH: str = pkg_resources.resource_filename("schug", GENES_37)
GENES_38_PATH: str = pkg_resources.resource_filename("schug", GENES_38)
TRANSCRIPTS_37_PATH: str = pkg_resources.resource_filename("schug", TRANCRIPTS_37)
TRANSCRIPTS_38_PATH: str = pkg_resources.resource_filename("schug", TRANCRIPTS_38)
