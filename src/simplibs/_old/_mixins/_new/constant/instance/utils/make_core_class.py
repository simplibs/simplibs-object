from typing import Any

def make_atom_core_class(base_class: type) -> type:
    """
    Externí továrna na CORE třídy (hodnotová jádra).
    Vytváří třídu, která nese stav a využívá logiku základní definice.
    """

    def __init__(self, new_value: Any = None):
        # normalize máme k dispozici díky dědičnosti z base_class
        self._value = self.normalize(new_value, process_none=True)

    def getter(self) -> Any:
        return self._value

    def setter(self, new_value: Any) -> None:
        # Validace a zápis
        self._value = self.normalize(new_value, process_none=True)

    class_name = f"{base_class.__name__}Core"
    class_parents = (base_class,)

    class_dict = {
        '__doc__': f"CORE jádro pro definici {base_class.__name__}",
        '__slots__': ("_value",),
        '__init__': __init__,
        'value': property(getter, setter),
    }

    return type(class_name, class_parents, class_dict)