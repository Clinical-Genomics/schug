from enum import Enum
from typing import Optional


class Build(str, Enum):
    build_37 = "37"
    build_38 = "38"

    @classmethod
    def _missing_(cls, value) -> Optional[Enum]:
        """Force GRCh37 and GRCh38 values into accepted formats."""
        for member in cls:
            if member in value:
                return member
        return None
