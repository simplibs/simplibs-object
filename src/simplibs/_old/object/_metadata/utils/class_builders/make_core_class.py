from typing import Any
# Outers
from ...._types import SimpleClassType

def make_core_class(
    owner_class: SimpleClassType
) -> type:
    """
    Externí továrna na CORE třídy (hodnotová jádra).
    Vytváří třídu, která nese stav a využívá logiku základní definice.
    """

    # 1. Definice inicializačního procesu
    def __init__(self, new_value: Any = None):
        # normalize máme k dispozici díky dědičnosti z owner_class
        self._value = self.normalize(new_value, process_none=True)

    # 2. Definice geteru
    def getter(self) -> Any:
        return self._value

    # 3. Definice setteru
    def setter(self, new_value: Any) -> None:
        # Validace a zápis
        self._value = self.normalize(new_value, process_none=True)

    # 4. Definice jména třídy
    class_name = f"{owner_class.__name__}Core"

    # 5. Definice předka (třífy pro kteoruje value určena)
    class_parents = (owner_class,)

    # 6. Vytvoření slovníku třídy
    class_dict = {
        '__doc__': f"CORE jádro pro definici {owner_class.__name__}",
        '__slots__': ("_value",),
        '__init__': __init__,
        'value': property(getter, setter),
    }

    # 7. Vytvoření a navrácení ohbjektu
    return type(class_name, class_parents, class_dict)