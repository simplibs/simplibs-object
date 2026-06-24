from typing import Any
from operator import attrgetter
# Outers
from ....protocols import SimpleMetadataType
# Inners
from .validations import raise_class_not_decomposeable


def create_inner_composite_property(
    inner_meta: SimpleMetadataType,
    path: tuple[str, ...],
    *,
    mutable: bool = True
) -> property:
    """
    Vytváří property pro kompozitní inner.

    - Getter vždy vrací hodnotu kompozice.
    - Setter se generuje pouze pokud je `mutable=True` a kompozice
      podporuje dekompozici (`is_decomposeable=True`).

    V immutable režimu se vrací pouze getter bez setteru.
    """

    # 1. Docstring pro imutable
    doc_string = (
        f"Hodnota typu `{inner_meta.value_type_name}`.\n"
        f"\n"
        f"Getter vrací hodnotu kompozice uloženou ve vnitřním slotu `{inner_meta.name_private}`.\n"
    )

    # 2. Definice pomocné funkce pro rychlý přístup k privátnímu slotu instance
    get_inner_instance = attrgetter(*path)

    # 3. Definice Getteru
    def getter(self) -> Any:
        return get_inner_instance(self).value

    # 4. Definice anotace getteru
    getter.__annotations__ = {"return": inner_meta.value_type}

    # 5. Návrat pro imutable
    if not mutable:
        return property(fget=getter, doc=doc_string)

    # 6. Definice Setteru
    def setter(self, value: Any) -> None:

        # 6.1 Získání instance
        inner_instance = get_inner_instance(self)

        # 6.2 Ověření, zda tato kompozice podporuje dekompozici
        if not inner_meta.is_decomposeable:
            raise_class_not_decomposeable(inner_meta)

        # 6.3 Zápis hodnoty a aktivace přepočtu ownera
        # noinspection PyProtectedMember
        inner_instance._root_value_setter(value, recalculate_up=True)

        # 6.4 Rozložení hodnoty a zápis do vnitřních prvků
        # noinspection PyProtectedMember
        inner_instance._recalculate_inners()

    # 7. Definice anotace setteru
    setter.__annotations__ = {"value": inner_meta.value_type, "return": None}

    # 8. Docstrin pro mutable
    doc_string += (
        "Setter provádí normalizaci hodnoty, uložení a spouští aktualizační kaskádu směrem nahoru."
    )

    # 9. Sestavení property
    return property(
        fget=getter,
        fset=setter,
        doc=doc_string
    )
