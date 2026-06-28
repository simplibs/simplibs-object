from typing import TYPE_CHECKING
# Inners
from ._collect_stepper_properties import _collect_stepper_properties
# Annotations
if TYPE_CHECKING:
    from .....protocols.metadata import SimpleMetadataLike



def collect_all_stepper_properties(
    meta: "SimpleMetadataLike"
) -> dict:
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