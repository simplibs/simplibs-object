from typing import Any
from operator import attrgetter
# Outers
from ....._types import SimpleMetaType


def create_inner_atom_property(
    inner_meta: SimpleMetaType,
) -> property:
    """
    Vytváří plnohodnotnou property (getter/setter) pro přístup k vnitřnímu slotu.
    Uzamkne název atributu do closure pro maximální čitelnost a rychlost.
    """

    # 1. Definice pomocné funkce pro rychlý přístup k privátnímu slotu instance
    get_inner_instance = attrgetter(inner_meta.name_private)

    # 2. Definice Getteru
    def getter(self) -> Any:
        return get_inner_instance(self).value

    # 3. Definice anotace getteru
    getter.__annotations__ = {"return": inner_meta.value_type}

    # 4. Definice Setteru
    def setter(self, value: Any) -> None:

        # 4.1 Získání instance
        inner_instance = get_inner_instance(self)

        # 4.2 Zápis hodnoty a aktivace přepočtu ownera
        # noinspection PyProtectedMember
        inner_instance._root_value_setter(value, recalculate_up=True)

    # 5. Definice anotace setteru
    setter.__annotations__ = {"value": inner_meta.value_type, "return": None}

    # 6. Definice docstringu
    doc_string = (
        f"Hodnota typu `{inner_meta.value_type.__name__}`.\n"
        f"\n"
        f"Getter vrací normalizovanou hodnotu uloženou ve vnitřním slotu `{inner_meta.name_snake}`.\n"
        f"Setter provádí normalizaci hodoty, uložení a spouští aktualizační kaskádu směrem nahoru."
    )

    # 7. Sestavení a navrácení hotové property
    return property(
        fget=getter,
        fset=setter,
        doc=doc_string
    )