# Outers
from ...._types import SimpleMetaType
# Inners
from .property_helpers.create_atom_property import create_atom_property
from .property_helpers.create_composite_property import create_composite_property
from .composite_helpers.collect_slots import collect_slots
from .composite_helpers.create_init import create_init
from .composite_helpers.create_repr import create_repr
from .composite_helpers.create_recalculate_up import create_recalculate_up


def make_composite_class(
    meta: SimpleMetaType
) -> type:
    """
    Orchestrátor pro tvorbu kompozitní instanční třídy (Node).
    Skládá dynamické sloty, inicializační logiku a přístupové cesty.
    """

    # 1. Defnice jména třídy
    class_name = meta.instance_name

    # 2. Definice předků třídy
    class_parents = (meta.atom_class,)

    # 3. Definice slovníku třídy
    class_dict = {
        "__doc__": f"Kompozitní instanční objekt pro {meta.class_name}",
        "__slots__": collect_slots(meta),
        "__init__": create_init(meta),
        "__repr__": create_repr(meta),
        "_recalculate_up": create_recalculate_up(meta),
        "value": create_composite_property(meta),
    }

    # 4. Přidání property pro konstanty
    for name_snake, const_meta in meta.constants_map.items():
        class_dict[name_snake] = create_atom_property(const_meta)

    # 5. Přidání property pro kompozice
    for name_snake, comp_meta in meta.composites_map.items():
        class_dict[name_snake] = create_composite_property(comp_meta)

    # 4. Vytvoření a nevrácení třídy
    return type(
        class_name,
        class_parents,
        class_dict
    )