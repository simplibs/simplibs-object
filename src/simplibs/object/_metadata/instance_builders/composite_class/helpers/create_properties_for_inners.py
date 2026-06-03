# Outers
from ....._types import SimpleMetaType
from ....._utils.properties import create_properties_for_inner


def create_properties_for_inners(
    meta: SimpleMetaType,
) -> dict:
    """Generuje slovník přístupových vlastností (properties) pro všechny přímé inners."""

    # 1. Definice prázdného slovníku
    property_dict = {}

    # 2. Zpracování innerů
    for inner in meta.inners:
        properties = create_properties_for_inner(inner.meta)
        property_dict.update(properties)

    # 3. Navrácení slovníku s property
    return property_dict