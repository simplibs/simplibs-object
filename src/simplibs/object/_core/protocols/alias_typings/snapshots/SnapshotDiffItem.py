from typing import TypeAlias, Any


# Single change record: triplet (element_path, old_value, new_value)
SnapshotDiffItem: TypeAlias = tuple[str, Any, Any]