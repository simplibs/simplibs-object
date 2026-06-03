# Outers
from ....._types import SimpleMetaType


def collect_slots(
    meta: SimpleMetaType
) -> tuple[str, ...]:
    """
    Vytvoří n-tici jmen slotů pro vnitřní prvky kompozice.

    Sloty pro '_value' a '__weakref__' se zde NEUVÁDĚJÍ, 
    protože jsou automaticky poděděny z atomické třídy.
    """

    # 1. Definice kontejneru
    slots = []

    # 2. Přidání slotů pro konstanty (Atomy)
    for const_meta in meta.constants_map.values():
        slots.append(const_meta.name_private)

    # 3. Přidání slotů pro kompozice (Nodes)
    for comp_meta in meta.composites_map.values():
        slots.append(comp_meta.name_private)

    # 4. Převod na tuple a návrat hodnoty
    return tuple(slots)