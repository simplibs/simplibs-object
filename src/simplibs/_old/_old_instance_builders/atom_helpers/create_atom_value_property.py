from typing import Any
# Outers
from ...._types import SimpleMetaType


def create_atom_value_property(
    meta: SimpleMetaType,
) -> property:
    """
    Vytváří plnohodnotnou property (getter/setter) pro přístup k vnitřnímu slotu _value.
    """

    # 1. Definice Getteru
    def getter(self) -> Any:
        return self._value

    # 2. Definice anotace getteru
    getter.__annotations__ = {"return": meta.value_type}

    # 3. Definice Setteru
    def setter(self, value: Any) -> None:

        # 3.1 Zápis hodnoty a aktivace přepočtu ownera
        self._root_value_setter(value, recalculate_up=True)

    # 4. Definice anotace setteru
    setter.__annotations__ = {"value": meta.value_type, "return": None}

    # 5. Definice docstringu
    doc_string = (
        f"Hodnota typu `{meta.value_type.__name__}`.\n"
        f"\n"
        f"Getter vrací hodnotu kterou třída reprezentuje.\n"
        f"Setter provádí normalizaci hodoty, uložení a spouští aktualizační kaskádu směrem nahoru."
    )

    # 6. Sestavení a navrácení hotové property
    return property(
        fget=getter,
        fset=setter,
        doc=doc_string
    )