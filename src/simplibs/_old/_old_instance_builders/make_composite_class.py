# Outers
from ..._types import SimpleMetaType
# Inners
from .composite_helpers import (
    create_composite_init,
    create_recalculate_self,
    create_recalculate_inners,
    create_composite_value_property,
    create_properties_for_inners
)


def make_composite_class(
    meta: SimpleMetaType
) -> type:
    """
    Orchestrátor pro tvorbu kompozitní instanční třídy (Node).
    Skládá dynamické sloty, inicializační logiku a přístupové cesty.
    """

    # 1. Defnice jména třídy
    base_class_name = f"{meta.class_name}CompositeBase"

    # 2. Definice předků třídy
    class_parents = (meta.atom_class,)

    # 3. Definice slovníku třídy
    class_dict = {
        "__doc__": f"Kompozitní instanční objekt pro {meta.class_name}",
        "__slots__": tuple(inner.meta.name_private for inner in meta.inners),
        "__init__": create_composite_init(meta, base_class_name),
        "_recalculate_self": create_recalculate_self(meta, base_class_name),
        "_recalculate_inners": create_recalculate_inners(meta, base_class_name),
        "value": create_composite_value_property(meta),
    } | create_properties_for_inners(meta)

    # 4. Vytvoření třídy
    composite_class = type(
        base_class_name,
        class_parents,
        class_dict
    )

    # 5. Odstranění deklarativních atributů
    for name in ("inners", "_logic", "_decompose"):
        if hasattr(composite_class, name):
            delattr(composite_class, name)

    # 6. Navrácení třídy
    return composite_class


class PropertyMixin:
    # Vytvořit mixin který zpřístupní vnitnří prvky z inners
    # 1. Definice kontejneru
    slots = []

    # 2. Přidání slotů pro konstanty (Atomy)
    for const_meta in meta.constants_map.values():
        slots.append(const_meta.name_private)

    # 3. Přidání slotů pro kompozice (Nodes)
    for comp_meta in meta.composites_map.values():
        slots.append(comp_meta.name_private)

    class_dict = {}

    # 4. Přidání property pro konstanty
    for name_snake, const_meta in meta.constants_map.items():
        class_dict[name_snake] = create_atom_property(const_meta)

    # 5. Přidání property pro kompozice
    for name_snake, comp_meta in meta.composites_map.items():
        class_dict[name_snake] = create_composite_property(comp_meta)