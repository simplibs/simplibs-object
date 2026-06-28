from typing import TypeAlias, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .SnapshotDiffItem import SnapshotDiffItem


# N-tice všech detekovaných změn v objektu
SnapshotDiffTuple: TypeAlias = tuple["SnapshotDiffItem", ...]