from typing import TypeAlias, TYPE_CHECKING, Mapping
# Annotations
if TYPE_CHECKING:
    from .PathTuple import PathTuple


# Mapa přiřazující snake_case názvu poduzlu jeho relativní hierarchickou cestu
NodesPathDict: TypeAlias = Mapping[str, "PathTuple"]