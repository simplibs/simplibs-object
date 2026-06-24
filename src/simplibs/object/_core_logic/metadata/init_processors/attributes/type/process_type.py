from simplibs.sentinels import UNSET
from types import NoneType, UnionType
from functools import reduce
from operator import or_
from simplibs.sentinels import UNSET
# Outers
from .....protocols import SimpleClassType
# Inners
from .validations.type import (
    validate_type_is_defined,
    validate_type_is_not_none,
    validate_type_is_not_empty,
    raise_validate_type_is_not_valid,
)
from .validations.tuple import (
    validate_type_from_tuple_is_not_none,
    validate_type_tuple_is_not_nested
)
from .validations.union import raise_union_type_contain_none


def process_type(
    owner_class: SimpleClassType,
) -> tuple[type | UnionType, str]:
    """
    Validuje integritu definice typu a transformuje tuple na moderní UnionType.

    Garantuje, že výsledek neobsahuje None/NoneType a je kompatibilní
    s typovými anotacemi i funkcí isinstance.
    """

    # 1. Získání atributu
    raw_type = getattr(owner_class, "_type", UNSET)

    # 2. Základní validace
    if not raw_type:
        validate_type_is_defined(raw_type, owner_class)
        validate_type_is_not_none(raw_type, owner_class)
        validate_type_is_not_empty(raw_type, owner_class)

    # 3. Zpracování atomického typu
    if isinstance(raw_type, type):
        return  raw_type, raw_type.__name__

    # 4. Zpracování UnionType
    if isinstance(raw_type, UnionType):

        # 4.1 Kontrola zda neobsahuje None
        if NoneType in raw_type.__args__:
            raise_union_type_contain_none(owner_class)

        # 4.2 Navrácení UnionType
        return raw_type, str(raw_type)

    # 5. Zpracování tuple (transformace na UnionType)
    if isinstance(raw_type, tuple):

        # 5.1 Kontrola vnitřních prvků
        valid_types = []
        for inner_type in raw_type:

            # 5.1.1 Kontrola typu
            if isinstance(inner_type, tuple) or inner_type is None:
                validate_type_tuple_is_not_nested(inner_type, raw_type, owner_class)
                validate_type_from_tuple_is_not_none(inner_type, raw_type, owner_class)

            # 5.1.2 Přidání typu
            valid_types.append(inner_type)

        # 5.2 Navrácení UnionType (int | str | float)
        final_type = reduce(or_, valid_types)
        return final_type, str(final_type)

    # 6. Vyvolání výjimky pro neplatně zadaný typ
    raise_validate_type_is_not_valid(raw_type, owner_class)
