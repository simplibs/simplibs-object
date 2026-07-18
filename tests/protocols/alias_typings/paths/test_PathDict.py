from typing import TypeAlias, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .PathTuple import PathTuple


# Celkový sekvenční registr všech sub-node prvků kompozice
PathDict: TypeAlias = dict[str, "PathTuple"]