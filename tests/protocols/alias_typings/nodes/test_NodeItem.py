from typing import TypeAlias, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ...instance import SimpleInstanceLike
    from ..paths import PathTuple


# Jedna položka v registru: dvojice (živá_instance, její_cesta)
NodeItem: TypeAlias = tuple["SimpleInstanceLike", "PathTuple"]