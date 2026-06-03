# Outers
from ...._types import SimpleMetaType
# Inners
from .property_helpers import (
    create_inner_atom_property,
    create_inner_composite_property
)


def create_properties_for_inners(
    meta: SimpleMetaType
) -> dict:
    """Generuje slovník přístupových vlastností (properties) pro všechny přímé inners."""

    # 1. Definice prázdného slovníku
    property_dict = {}

    # 2. Zpracování innerů
    for inner in meta.inners:

        # 2.1 Vtyažení meta pro snadnější přístup
        inner_meta = inner.meta

        # 2.2 Vytvoření property pro konstantu
        if inner_meta.is_constant:
            param_property = create_inner_atom_property(inner_meta)

        # 2.3 Vytvoření property pro kompozici
        else:
            param_property = create_inner_composite_property(inner_meta)

        # 2.4 Přidání property do slovníku
        property_dict[inner_meta.name_snake] = param_property

    # 3. Navrácení slovníku s property
    return property_dict