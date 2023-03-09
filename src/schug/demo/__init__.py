import pkg_resources

# Filenames
EXONS_37 = "demo/exons_37.tsv"
EXONS_38 = "demo/exons_38.tsv"
GENES_37 = "demo/genes_37.tsv"
GENES_38 = "demo/genes_38.tsv"
TRANCRIPTS_37 = "demo/transcripts_37.tsv"
TRANCRIPTS_38 = "demo/transcripts_38.tsv"

# Paths
EXONS_37_PATH = pkg_resources.resource_filename("schug", EXONS_37)
EXONS_38_PATH = pkg_resources.resource_filename("schug", EXONS_38)
GENES_37_PATH = pkg_resources.resource_filename("schug", GENES_37)
GENES_38_PATH = pkg_resources.resource_filename("schug", GENES_38)
TRANSCRIPTS_37_PATH = pkg_resources.resource_filename("schug", TRANCRIPTS_37)
TRANSCRIPTS_38_PATH = pkg_resources.resource_filename("schug", TRANCRIPTS_38)
