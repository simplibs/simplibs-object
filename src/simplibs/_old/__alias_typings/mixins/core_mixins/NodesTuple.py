from typing import TypeAlias, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .NodeItem import NodeItem


# Celkový sekvenční registr všech sub-node prvků kompozice
NodesTuple: TypeAlias = tuple["NodeItem", ...]