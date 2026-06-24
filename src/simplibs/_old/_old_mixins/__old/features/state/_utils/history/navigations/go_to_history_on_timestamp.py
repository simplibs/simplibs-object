from datetime import datetime
# Outers
from .._validations import raise_unvalide_timestamp, raise_unvalide_snopshot_timestamp


def go_to_history_on_timestamp(self, timestamp: datetime):
    """Metoda pro přechod na konkrétní timestamp"""

    # 1. Validace zadané hodnoty
    if not isinstance(timestamp, datetime):
        raise_unvalide_timestamp()

    # 2. Pokus o nalezení snapshotu
    for i, (ts, snapshot) in enumerate(self._history):
        if ts == timestamp:
            self._history_index = i
            self._restore_snapshot(snapshot)
            return True

    # 3. Výjimky když nebyl timestamp nalezen
    raise_unvalide_snopshot_timestamp()
    return False
