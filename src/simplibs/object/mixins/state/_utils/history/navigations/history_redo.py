def history_redo(self) -> bool:
    """Metodea pro přechod na následující záznam (pokud existuje)."""

    # 1. Kontrola zda je kam jít
    if self._history_index >= self._history_count - 1:
        return False

    # 2. Přechod na následující záznam
    self._history_index += 1
    _, snapshot = self._history[self._history_index]
    self._restore_snapshot(snapshot)
    return True