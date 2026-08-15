from typing import TypeAlias, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .NodeItem import NodeItem


# Complete sequential registry of all subnode elements in a composition
NodesTuple: TypeAlias = tuple["NodeItem", ...]