from typing import TypeAlias, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .DirtyPathItem import DirtyPathItem


# N-tice všech detekovaných změn v objektu
DirtyPathsTuple: TypeAlias = tuple["DirtyPathItem", ...]