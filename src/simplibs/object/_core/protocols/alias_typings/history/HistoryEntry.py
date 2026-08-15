from typing import TypeAlias, TYPE_CHECKING
from datetime import datetime
# Annotations
if TYPE_CHECKING:
    from ..snapshots import SnapshotTuple


# Represents a single timestamped state record on the history timeline
HistoryEntry: TypeAlias = tuple[datetime, "SnapshotTuple"]

