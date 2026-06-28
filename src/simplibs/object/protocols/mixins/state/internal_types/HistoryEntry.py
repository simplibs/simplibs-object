from typing import TypeAlias, TYPE_CHECKING
from datetime import datetime
# Annotations
if TYPE_CHECKING:
    from ....alias_typings import SnapshotTuple


# Jeden zápis historie
HistoryEntry: TypeAlias = tuple[datetime, "SnapshotTuple"]

