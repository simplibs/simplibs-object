from typing import TypeAlias, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .PathTuple import PathTuple


# Complete sequential registry mapping node keys to their path tuples
PathDict: TypeAlias = dict[str, "PathTuple"]