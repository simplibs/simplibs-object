from typing import Callable
# Outers
from ....._types import SimpleMetaType


def create_repr(
    meta: SimpleMetaType
) -> Callable:
    """
    Vytváří reprezentaci, která vypadá jako volání třídy.
    Výsledek: Color(value='red')
    """

    # 1. Definice metody
    def __repr__(self):

        # 1.1 Navrácení řetězce s jménem tířdy a hodotu
        return f"{meta.class_name}(value={self._value!r})"

    # 2. Navrácení metody
    return __repr__

