from typing import TypeAlias, TYPE_CHECKING
from collections.abc import Mapping
# Annotations
if TYPE_CHECKING:
    from ...instance import SimpleInstanceLike
    from ..paths import PathTuple


# Komplexní mapa propojující snake_case název uzlu s jeho živou instancí a cestou
NodesDict: TypeAlias = Mapping[str, tuple["SimpleInstanceLike", "PathTuple"]]