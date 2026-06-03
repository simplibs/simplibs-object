from simplibs.sentinels import UNSET
# Oouters
from ....._types import SimpleClassType
# Inners
from .validations.constant import (
    validate_default_matches_annotation,
    validate_default_is_defined,
)


def process_default_for_constant(
    default_type,
    owner_class: SimpleClassType,
):

    # 1. Natažení defaultu
    row_default = getattr(owner_class, "_default", UNSET)

    # 2. Kontrola validity
    if (row_default is UNSET or
        not isinstance(row_default, default_type)):
        validate_default_is_defined(row_default, owner_class)
        validate_default_matches_annotation(row_default, default_type, owner_class)

    # 3. Navrácení defaultu
    return row_default



