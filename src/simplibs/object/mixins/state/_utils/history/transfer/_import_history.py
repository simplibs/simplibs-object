from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ......protocols.mixins.state import HistoryProtocol


def _import_history(
    self: "HistoryProtocol",
    history_list: list
) -> None:
    """Importuje historii. Při chybě obnoví původní stav."""

    # 1. Záloha předchozího stavu
    backup = self._history

    # 2. Nahrazení historie
    try:

        # 2.1 Přidání hisotorie
        self._history = list(history_list)

        # 2.2 Přechod na poslední historii
        self.go_to_last()

        # 2.3 případné oříznutí historie (dle limitu, je-li nastaven)
        if self.history_limit:
            self.history_limit = self.history_limit

    # 3. Zachycení výjimek (návrat do původního stavu)
    except Exception as e:

        # 3.1 Načtení zálohy
        self._history = backup

        # 3.2 Přechod na poslední historii
        self.go_to_last()

        # 3.2 Vyvolání zachycené výjimky
        raise e