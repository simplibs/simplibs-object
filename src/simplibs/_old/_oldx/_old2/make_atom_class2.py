from typing import Any
# Outers
from ...._types import SimpleClassProtocol
from .InstanceBase import InstanceBase


def make_atom_class(
    owner_class: type
) -> type:
    """
    Továrna na instance, vytváří finální třídu, kterou uživatel používá.
    """

    # 1. Definice inicializace (zatím pro konstantu)
    def __init__(self, new_value: Any = None):
        self._value = self.normalize(new_value, process_none=True)
        self._on_update()

    # 3. Definice geteru
    def getter(self) -> Any:
        return self._value

    # 4. Definice setteru
    def setter(self, new_value: Any) -> None:
        old_value = self._value
        new_normalized = self.normalize(new_value, process_none=True)

        if old_value != new_normalized:
            self._value = new_normalized
            self._on_update()

    # 6. Sestavení třídy
    class_name = f"{owner_class.__name__}Instance"
    class_parents = (InstanceBase, owner_class,)
    class_dict = {
        '__doc__': f"Instanční objekt pro {owner_class.__name__}",
        '__slots__': ("_value", "__weakref__"),  # Weakref pro pokročilé vazby
        '__init__': __init__,
        'value': property(getter, setter),
    }

    # 7. Vytvoření a navrácení ohbjektu
    return type(class_name, class_parents, class_dict)