from typing import TypeAlias, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ...instance import SimpleInstanceLike
    from ..paths import PathTuple


# Single item in registry: pair (live_instance, its_path)
NodeItem: TypeAlias = tuple["SimpleInstanceLike", "PathTuple"]