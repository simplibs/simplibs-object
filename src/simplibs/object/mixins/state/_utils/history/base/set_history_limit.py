from typing import TYPE_CHECKING
# Outers
from .._validations import raise_history_limit_not_positive_integer
# Annotations
if TYPE_CHECKING:
    from ......protocols.mixins.state import HistoryProtocol


def set_history_limit(
    self: "HistoryProtocol",
    value: int
) -> None:
    """Nastaví hodnotu limitu velikosti historie"""

    # 1. Validace hodnoty
    if not isinstance(value, int) or value < 1:
        raise_history_limit_not_positive_integer()

    # 2. Přizpůsobení historie limitu
    if self._history_count > value:
        del self._history[:(self._history_count - value)]
        self._history_count = len(self._history)
        self._history_index = self._history_count - 1

    # 3. Zápis limitu
    self._history_limit = value
