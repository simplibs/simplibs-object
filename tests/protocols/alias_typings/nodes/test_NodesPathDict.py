from typing import TypeAlias, TYPE_CHECKING
from collections.abc import Mapping
# Annotations
if TYPE_CHECKING:
    from ..paths import PathTuple


# Mapa přiřazující snake_case názvu poduzlu jeho relativní hierarchickou cestu
NodesPathDict: TypeAlias = Mapping[str, "PathTuple"]