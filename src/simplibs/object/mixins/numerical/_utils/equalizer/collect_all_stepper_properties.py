# Outers
from ......protocols import SimpleMetadataType
# Inners
from ._collect_stepper_properties import _collect_stepper_properties


def collect_all_stepper_properties(meta: SimpleMetadataType) -> dict:
    """Vrátí slovník stepper property pro všechny inners (přímé i nested)."""

    # 1. Definice množiny pro property
    result = {}

    # 2. Průchod skrze vlastní inners
    for inner in meta.inners:

        # 1.1 Definice proměných
        inner_meta = inner.meta
        path = (inner_meta.name_private,)

        # 2.2.2 Rekurzivní zběr property pro vnitřní prvky
        _collect_stepper_properties(inner_meta, path, result)

    # 3. Navrácení množiny pro property
    return result