from typing import TypeAlias, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .HistoryRecord import HistoryRecord


# Neměnná časová osa tvořená záznamy historie
HistoryTimeline: TypeAlias = tuple["HistoryRecord", ...]