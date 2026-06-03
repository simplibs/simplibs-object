from typing import Any
from operator import attrgetter
# Outers
from ....._types import SimpleMetaType


def create_inner_composite_property(
    inner_meta: SimpleMetaType,
) -> property:
    """
    Vytváří plnohodnotnou property (getter/setter) pro přístup ke kompozitní hodnotě.
    Getter vrací hodnotu kompozice (self.<private>.value).
    Setter je povolen pouze pokud kompozice definuje decompose_value.
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

        # 4.2 Ověření, zda tato kompozice podporuje dekompozici
        if not inner_meta.is_decomposeable:
            raise TypeError(
                f"Kompozice '{inner_meta.class_name}' nepodporuje přímé přiřazení hodnoty, "
                f"protože nemá definovanou uživatelskou metodu decompose_value()."
            )

        # 4.3 Zápis hodnoty a aktivace přepočtu ownera
        # noinspection PyProtectedMember
        inner_instance._root_value_setter(value, recalculate_up=True)

        # 4.4 Rozložení hodnoty a zápis do vnitřních prvků
        # noinspection PyProtectedMember
        inner_instance._recalculate_inners()

    # 5. Definice anotace setteru
    setter.__annotations__ = {"value": inner_meta.value_type, "return": None}

    # 6. Docstring
    doc_string = (
        f"Hodnota typu `{inner_meta.value_type.__name__}`.\n"
        f"\n"
        f"Getter vrací hodnotu kompozice uloženou ve vnitřním slotu `{inner_meta.name_private}`.\n"
        f"Setter je povolen pouze pokud kompozice definuje `decompose_value`, jinak vyvolá chybu."
    )

    # 7. Sestavení property
    return property(
        fget=getter,
        fset=setter,
        doc=doc_string
    )
