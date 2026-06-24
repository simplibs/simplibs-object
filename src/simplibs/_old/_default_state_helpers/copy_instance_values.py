# Outers
from ...._types import SimpleInstanceType
# Inners
from ._process_copy import _process_copy


# noinspection PyProtectedMember
def copy_instance_values(
    source: SimpleInstanceType,
    target: SimpleInstanceType
) -> None:
    """
    Zkopíruje hodnoty všech atomů a kompozic z jiné instance.
    Rekurzivní, deterministické, bez validací.
    """

    # 1. Kopírování atomů
    for const_meta in target._constants_map.values():
        _process_copy(source, target, const_meta)

    # 2. Kopírování kompozic (rekurzivně)
    for comp_meta in target._composites_map.values():
        _process_copy(source, target, comp_meta, recurse=True)

    # 3. Kopírování hlavní hodnoty kompozice
    target._value = source._value

