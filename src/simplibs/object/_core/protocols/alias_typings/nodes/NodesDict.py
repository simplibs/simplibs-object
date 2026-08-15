from typing import TypeAlias, TYPE_CHECKING, Mapping
# Annotations
if TYPE_CHECKING:
    from ...instance import SimpleInstanceLike
    from ..paths import PathTuple


# Complex map connecting snake_case node name to its live instance and path
NodesDict: TypeAlias = Mapping[str, tuple["SimpleInstanceLike", "PathTuple"]]