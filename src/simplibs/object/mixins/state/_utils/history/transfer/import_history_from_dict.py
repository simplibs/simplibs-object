from typing import TYPE_CHECKING, Any
from simplibs.sentinels import UNSET
# Outers
from ....._common.constants import (
    OWNER_CLASS,
    HISTORY,
)
# Annotations
if TYPE_CHECKING:
    from ......protocols.mixins.state import HistoryProtocol


def import_history_from_dict(
    self: "HistoryProtocol",
    history_dict: dict[str, Any]
) -> None:
    """Importuje historii z přenositelného formátu s kontrolou owner_class."""

    # 1. Validace vstupu
    if not isinstance(history_dict, dict):
        raise TypeError("Input must be a dictionary.")

    # 2. Validace owner class
    owner_class = history_dict.get(OWNER_CLASS, UNSET)
    if self.meta.owner_class != owner_class:
        raise ValueError(
            f"Owner class mismatch. Expected: {self.meta.owner_class}, Got: {owner_class}"
        )

    # 3. Záloha předchozího stavu
    backup = self._history

    # 4. Převod historie
    try:

        # 4.1 Nahrazení historie
        self._history = list(history_dict[HISTORY])
        self.go_to_last()

        # 4.1 Případné oříznutí historie (dle limitu, je-li nastaven)
        if self.history_limit:
            self.history_limit = self.history_limit

    # 5. Zachycení výjimek (návrat do původního stavu)
    except Exception as e:

        # 5.1 Obnovení stavu
        self._history = backup
        self.go_to_last()

        # 5.2 Vyvolání zachycené výjimky
        raise e
