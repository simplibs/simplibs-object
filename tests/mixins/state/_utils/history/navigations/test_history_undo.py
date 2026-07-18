from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ......protocols.mixins.state import HistoryProtocol


def history_undo(
    self: "HistoryProtocol"
) -> bool:
    """Metodea pro přechod na předchozí záznam (pokud existuje)."""

    # 1. Kontrola zda je kam jít
    if self._history_index <= 0:
        return False

    # 2. Přechod na předchozí záznam
    self._history_index -= 1
    _, snapshot = self._history[self._history_index]
    self._restore_snapshot(snapshot)
    return True