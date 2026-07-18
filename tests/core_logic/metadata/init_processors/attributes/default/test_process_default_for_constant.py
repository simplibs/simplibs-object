from typing import Any, TYPE_CHECKING
from types import UnionType
from simplibs.sentinels import UNSET
# Inners
from .validations.constant import (
    validate_default_matches_annotation,
    validate_default_is_defined,
)
# Annotations
if TYPE_CHECKING:
    from ......protocols.classes import SimpleClassLike


def process_default_for_constant(
    default_type: type | UnionType,
    owner_class: "SimpleClassLike",
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



