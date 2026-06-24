def go_to_last_history(self):
    """Metodea pro přechod na poslední záznam historie."""

    # 1. Kontrola zda tam už nejsme
    last_index = self._history_count - 1
    if self._history_index == last_index:
        return False

    # 2. Přechod na poslední záznam
    self._history_index = last_index
    _, snapshot = self._history[self._history_index]
    self._restore_snapshot(snapshot)
    return True