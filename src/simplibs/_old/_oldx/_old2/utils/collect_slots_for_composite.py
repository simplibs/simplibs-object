from ....._types import SimpleMetaType

def collect_slots_for_composite(
    meta: SimpleMetaType
) -> tuple[str, ...]:
    """Vytvoří n-tici jmen slotů pro všechny vnitřní instance."""

    # 1. Základní hodnota (zistit zda se toto nedění z knstantí třídy)
    slots = ["_value"]

    # 2. Přidáme sloty pro všechny konstanty
    for const_meta in meta.constants_map.values():
        slots.append(const_meta.name_private)

    # 3. Přidáme sloty pro všechny kompozice
    for comp_meta in meta.composites_map.values():
        slots.append(comp_meta.name_private)

    # 4. Navrácení hodnoty jako tuple
    return tuple(slots)