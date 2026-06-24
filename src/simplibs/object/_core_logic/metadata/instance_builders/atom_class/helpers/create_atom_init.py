from typing import Callable
from simplibs.sentinels import UNSET
# Outers
from .....protocols import SimpleMetadataType


def create_atom_init(
    meta: SimpleMetadataType,
    base_class_name: str
) -> Callable:
    """
    Vytváří inicializační metodu pro atomickou instanci.
    Propisuje metadata (default, typ) přímo do signatury funkce.
    """

    # 1. Definice logiky initu
    def __init__(self):

        # Vytvoření hodnoty z defaultu
        self._value = meta.default

        # Nastavení atributu pro vlastníka na UNSET (definuje až konstanta skrze své inners)
        self._owner = UNSET

        # Nastavení zámku hodnoty
        self._locked = False

        # Zpuštění pomocné metody pro mixiny (umožňující mixinům připsat logiku do initu)
        self.init_mixins()

    # 2. Dynamické přilepení metadat
    __init__.__name__ = "__init__"
    __init__.__qualname__ = f"{base_class_name}.__init__"
    __init__.__annotations__ = {"return": None}

    # 3. Navrácení metody
    return __init__