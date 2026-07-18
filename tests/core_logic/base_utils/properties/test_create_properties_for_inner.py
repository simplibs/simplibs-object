from typing import TYPE_CHECKING
# Inners
from .create_value_property import create_value_property
from .create_instance_property import create_instance_property
# Annotations
if TYPE_CHECKING:
    from ....protocols.metadata import SimpleMetadataLike
    from ....protocols.alias_typings import PathTuple


def create_properties_for_inner(
    inner_meta: "SimpleMetadataLike",
    path: "PathTuple | ()" = (),
    *,
    mutable: bool = True
) -> dict[str, property]:
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

    # 3. Vytvoření property
    value_property = create_value_property(
        inner_meta,
        is_constant=inner_meta.is_constant,
        mutable=mutable,
        path=instance_path
    )

    # 4. Vytvoření property pro přístup k instanci
    instance_property = create_instance_property(
        inner_meta,
        instance_path
    )

    # 5. Přidání property do slovníku
    property_dict[name_snake] = value_property
    property_dict[f"{name_snake}_instance"] = instance_property

    # 6. Navrácení slovníku s property
    return property_dict
