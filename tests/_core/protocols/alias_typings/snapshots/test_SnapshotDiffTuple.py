from typing import TypeAlias, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .SnapshotDiffItem import SnapshotDiffItem


# Tuple of all detected state differences in an object
SnapshotDiffTuple: TypeAlias = tuple["SnapshotDiffItem", ...]