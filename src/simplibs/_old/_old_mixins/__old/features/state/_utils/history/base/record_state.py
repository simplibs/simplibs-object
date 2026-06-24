from datetime import datetime


def record_state(self) -> datetime:
    """Vytvoří snapshot aktuálního stavu a uloží ho do historie."""

    # 1. Vytvoření timestamp a snapshotu
    timestamp = datetime.now()
    snapshot = self._build_snapshot()

    # 2. Kontrola limitu
    if self._history_limit and self._history_count >= self._history_limit:
        self._history.pop(0)

    # 3. Zápis do historie
    self._history.append((timestamp, snapshot))
    self._history_count = len(self._history)
    self._history_index = self._history_count - 1

    # 4. Navrácení záznamu
    return timestamp