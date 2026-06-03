from typing import Any
# Outers
from ...._types import SimpleClassProtocol


def make_atom_class(
    owner_class: type
) -> type:
    """
    Továrna na instance, vytváří finální třídu, kterou uživatel používá.
    """

    # 1. Definice inicializace (zatím pro konstantu)
    def __init__(self, new_value: Any = None):
        # normalize a metadata máme z owner_class
        self._value = self.normalize(new_value, process_none=True)
        # Hook pro budoucí kompozitní sledování
        self._on_update()

    # 2. Definice hooku (ve výchozím stavu prázdný)
    def _on_update(self) -> None:
        pass

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

    # 5. Reprezentace (pro tvé riziko v bodě 1 - čitelnost)
    def __repr__(self) -> str:
        return f"{owner_class.__name__}(value={repr(self._value)})"

    # 6. Sestavení třídy
    class_name = f"{owner_class.__name__}Instance"
    class_parents = (owner_class,)
    class_dict = {
        '__doc__': f"Instanční objekt pro {owner_class.__name__}",
        '__slots__': ("_value", "__weakref__"),  # Weakref pro pokročilé vazby
        '__init__': __init__,
        '__repr__': __repr__,
        '_on_update': _on_update,
        'value': property(getter, setter),
    }

    # 7. Vytvoření a navrácení ohbjektu
    return type(class_name, class_parents, class_dict)