from typing import TYPE_CHECKING, Any
from datetime import datetime
# Annotations
if TYPE_CHECKING:
    from ......protocols.mixins.state import HistoryProtocol
    from ......protocols.mixins.state.internal_types import HistoryEntry

def record_state(
    self: "HistoryProtocol"
) -> "HistoryEntry":
    """Vytvoří snapshot aktuálního stavu a uloží ho do historie."""

    # 1. Vytvoření timestamp a snapshotu
    timestamp = datetime.now()
    snapshot = self._build_snapshot()

    # 2. Kontrola limitu
    if self._history_limit and self._history_count >= self._history_limit:
        self._history.pop(0)

    # 3. Zápis do historie
    history_entry = (timestamp, snapshot)
    self._history.append(history_entry)
    self._history_count = len(self._history)
    self._history_index = self._history_count - 1

    # 4. Navrácení záznamu
    return history_entry