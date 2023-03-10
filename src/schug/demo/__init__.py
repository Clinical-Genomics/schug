from contextlib import ExitStack

import importlib_resources

file_manager = ExitStack()

# Filenames
EXONS_37: str = importlib_resources.files("schug") / "demo/exons_37.tsv"
EXONS_38: str = importlib_resources.files("schug") / "demo/exons_38.tsv"
GENES_37: str = importlib_resources.files("schug") / "demo/genes_37.tsv"
GENES_38: str = importlib_resources.files("schug") / "demo/genes_38.tsv"
TRANCRIPTS_37: str = importlib_resources.files("schug") / "demo/transcripts_37.tsv"
TRANCRIPTS_38: str = importlib_resources.files("schug") / "demo/transcripts_38.tsv"

# Paths
EXONS_37_PATH: str = file_manager.enter_context(importlib_resources.as_file(EXONS_37))
EXONS_38_PATH: str = file_manager.enter_context(importlib_resources.as_file(EXONS_38))
GENES_37_PATH: str = file_manager.enter_context(importlib_resources.as_file(GENES_37))
GENES_38_PATH: str = file_manager.enter_context(importlib_resources.as_file(GENES_38))
TRANSCRIPTS_37_PATH: str = file_manager.enter_context(importlib_resources.as_file(TRANCRIPTS_37))
TRANSCRIPTS_38_PATH: str = file_manager.enter_context(importlib_resources.as_file(TRANCRIPTS_38))
