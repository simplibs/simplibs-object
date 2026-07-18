from typing import TypeAlias, TYPE_CHECKING
from datetime import datetime
# Annotations
if TYPE_CHECKING:
    from ..snapshots import SnapshotTuple


# Reprezentuje jeden časový záznam stavu na ose historie
HistoryEntry: TypeAlias = tuple[datetime, "SnapshotTuple"]

