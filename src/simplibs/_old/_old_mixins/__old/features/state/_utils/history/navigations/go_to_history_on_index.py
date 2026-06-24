# Outers
from .._validations import raise_unvalide_snapshot_index


def go_to_history_on_index(self, index: int):
    """Metoda pro přechod na konkrétní index"""

    # 1. Validace zadané hodnoty
    if not (0 <= index < self._history_count):
        raise_unvalide_snapshot_index()

    # 2. Přechod na záznam dle indexu
    self._history_index = index
    _, snapshot = self._history[self._history_index]
    self._restore_snapshot(snapshot)
    return True
