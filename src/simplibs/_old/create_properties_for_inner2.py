# Outers
from ...protocols import SimpleMetadataType
# Inners
from .helpers import (
    create_inner_atom_property,
    create_inner_composite_property,
    create_inner_instance_property
)


def create_properties_for_inner(
    inner_meta: SimpleMetadataType,
    path: tuple[str, ...] = (),
    *,
    mutable: bool = True
) -> dict:
    """
    Generuje dvojici properties pro jeden inner:

    - <name_snake>          → getter (a volitelně setter)
    - <name_snake>_instance → read‑only přístup k instanci inneru

    Parametr `mutable` určuje, zda se má generovat setter.
    V immutable režimu se vytváří pouze getter.
    """

    # 1. Definice prázdného slovníku
    property_dict = {}

    # 2 Vtvoření proměnných
    name_snake = inner_meta.name_snake
    instance_path = path + (inner_meta.name_private,)

    # 3. Vytvoření property pro konstantu
    if inner_meta.is_constant:
        param_property = create_inner_atom_property(inner_meta, instance_path, mutable=mutable)

    # 4. Vytvoření property pro kompozici
    else:
        param_property = create_inner_composite_property(inner_meta, instance_path, mutable=mutable)

    # 5. Vytvoření property pro přístup k instanci
    instance_property = create_inner_instance_property(inner_meta, instance_path)

    # 6. Přidání property do slovníku
    property_dict[name_snake] = param_property
    property_dict[f"{name_snake}_instance"] = instance_property

    # 7. Navrácení slovníku s property
    return property_dict
