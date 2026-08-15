from typing import TypeAlias, TYPE_CHECKING
from collections.abc import Mapping
# Annotations
if TYPE_CHECKING:
    from ..paths import PathTuple


# Map assigning a subnode snake_case name to its relative hierarchical path
NodesPathDict: TypeAlias = Mapping[str, "PathTuple"]