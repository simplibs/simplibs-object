from typing import Any, Union
from simplibs.sentinels import UNSET
# Outers
from .....protocols import SimpleClassType
# Inners
from .validations.constant import (
    validate_default_matches_annotation,
    validate_default_is_defined,
)


def process_default_for_constant(
    default_type: type | Union,
    owner_class: SimpleClassType,
) -> Any:

    # 1. Natažení defaultu
    raw_default = getattr(owner_class, "_default", UNSET)

    # 2. Kontrola validity
    if (raw_default is UNSET or
        not isinstance(raw_default, default_type)):
        validate_default_is_defined(raw_default, owner_class)
        validate_default_matches_annotation(raw_default, default_type, owner_class)

    # 3. Navrácení defaultu
    return raw_default



