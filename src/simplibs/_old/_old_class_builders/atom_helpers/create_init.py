from typing import Callable
# Outers
from ....._types import SimpleMetaType


def create_init(
    meta: SimpleMetaType
) -> Callable:
    """
    Vytváří inicializační metodu pro atomickou instanci.
    Propisuje metadata (default, typ) přímo do signatury funkce.
    """

    # 1. Definice logiky initu
    def __init__(self, value):
        self._value = self.normalize(value, process_none=True)
        self._owner = None

    # 2. Dynamické přilepení metadat
    __init__.__name__ = "__init__"
    __init__.__qualname__ = f"{meta.class_name}.__init__"
    __init__.__defaults__ = (meta.default,)
    __init__.__annotations__ = {
        "value": meta.value_type,
        "return": None
    }

    # 3. Navrácení metody
    return __init__