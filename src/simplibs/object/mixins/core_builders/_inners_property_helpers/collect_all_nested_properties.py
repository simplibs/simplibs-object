# Outers
from ...._types import SimpleMetaType
# Inners
from ._collect_nested_inner_properties import _collect_nested_inner_properties


def collect_all_nested_properties(
    meta: SimpleMetaType
) -> dict:
    """
    Vrátí slovník property pro všechny nested inners.
    Přímé inners se ignorují (ty už property mají).
    """

    # 1. Definice množiny pro property
    result = {}

    # 2. Průchod skrze vlastní inners
    for inner in meta.inners:

        # 2.1 Vytažení meta
        inner_meta = inner.meta

        # 2.2 Kontrola zda jde o kompozici
        if not inner_meta.is_constant:

            # 2.2.1 Vytvoření tuple pro cestu
            path = (inner_meta.name_private,)

            # 2.2.2 Rekurzivní zběr property pro vnitřní prvky
            _collect_nested_inner_properties(inner_meta, path, result)

    # 3. Navrácení množiny pro property
    return result
