# Outers
from ...protocols import SimpleMetadataType
# Inners
from .create_constant_property import create_constant_property
from .create_composite_property import create_composite_property
from .create_instance_property import create_instance_property



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
    """

    # 1. Definice prázdného slovníku
    property_dict = {}

    # 2 Vtvoření proměnných
    name_snake = inner_meta.name_snake
    instance_path = path + (inner_meta.name_private,)

    # 3. Vytvoření property pro konstantu
    if inner_meta.is_constant:
        value_property = create_constant_property(
            inner_meta,
            mutable=mutable,
            path=instance_path
        )

    # 4. Vytvoření property pro kompozici
    else:
        value_property = create_composite_property(
            inner_meta,
            mutable=mutable,
            path=instance_path
        )

    # 5. Vytvoření property pro přístup k instanci
    instance_property = create_instance_property(
        inner_meta,
        instance_path
    )

    # 6. Přidání property do slovníku
    property_dict[name_snake] = value_property
    property_dict[f"{name_snake}_instance"] = instance_property

    # 7. Navrácení slovníku s property
    return property_dict
