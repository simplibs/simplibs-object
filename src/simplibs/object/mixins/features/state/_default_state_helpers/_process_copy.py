# Outers
from ...._types import SimpleObjectInstanceType, SimpleMetaType


def _process_copy(
    source_instance: SimpleObjectInstanceType,
    target_instance: SimpleObjectInstanceType,
    meta: SimpleMetaType,
    recurse: bool = False
) -> None:

    # 1. Načtení instancí
    private_name = meta.name_private
    source_instance_attr = getattr(source_instance, private_name)
    target_instance_attr = getattr(target_instance, private_name)

    # 2. Změna hodnot
    # noinspection PyProtectedMember
    target_instance_attr._value = source_instance_attr._value

    # 3. Rekurzivní volání mateřské funkce
    if recurse:
        from .copy_instance_values import copy_instance_values
        copy_instance_values(source_instance_attr, target_instance_attr)
