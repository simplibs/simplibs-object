from typing import TYPE_CHECKING
from types import NoneType, UnionType
from functools import reduce
from operator import or_
from simplibs.sentinels import UNSET
# Inners
from .validations import (
    validate_type_is_defined,
    validate_type_is_not_none,
    validate_type_is_not_empty,
    raise_validate_type_is_not_valid,
    validate_type_from_tuple_is_not_none,
    validate_type_tuple_is_not_nested,
    raise_union_type_contain_none,
)
# Annotations
if TYPE_CHECKING:
    from ....protocols.classes import SimpleClassLike


def process_type(
    owner_class: "SimpleClassLike",
) -> tuple[type | UnionType, str]:
    """Validates and normalizes the '_type' attribute."""

    # 1. Fetch raw type
    raw_type = getattr(owner_class, "_type", UNSET)

    # 2. Early guards
    if raw_type is UNSET or not raw_type:
        validate_type_is_defined(raw_type, owner_class)
        validate_type_is_not_none(raw_type, owner_class)
        validate_type_is_not_empty(raw_type, owner_class)

    # 3. Atomic type
    if isinstance(raw_type, type):
        return raw_type, raw_type.__name__

    # 4. UnionType
    if isinstance(raw_type, UnionType):
        if NoneType in raw_type.__args__:
            raise_union_type_contain_none(owner_class)
        return raw_type, str(raw_type)

    # 5. Tuple of types
    if isinstance(raw_type, tuple):
        valid_types = []
        for inner_type in raw_type:
            if isinstance(inner_type, tuple) or inner_type is None:
                validate_type_tuple_is_not_nested(inner_type, raw_type, owner_class)
                validate_type_from_tuple_is_not_none(inner_type, raw_type, owner_class)
            valid_types.append(inner_type)

        final_type = reduce(or_, valid_types)
        return final_type, str(final_type)

    # 6. Fallback
    raise_validate_type_is_not_valid(raw_type, owner_class)



_DESIGN_NOTES = """
# process_type

## Purpose
Normalizes the `_type` attribute into a single, predictable runtime type.  
Supports three forms:

- atomic types (`int`, `str`, `MyClass`)
- modern UnionType (`int | str`)
- flat tuples (`(int, str)`)

All other forms are rejected.

## Pipeline overview

1. **Early guards**
   - `_type` must exist.
   - `_type` cannot be None.
   - `_type` cannot be empty.

2. **Atomic type**
   Fast path. Returns immediately.

3. **UnionType**
   - Must not contain `NoneType`.
   - Returned as-is.

4. **Tuple**
   - Must be flat.
   - Must not contain literal None.
   - Converted to a UnionType via `reduce(or_, ...)`.

5. **Fallback**
   Anything else is invalid.

## Why this normalization exists
The metadata system requires a single, concrete type object that can be used with:

- `isinstance(value, compiled_type)`
- validation routines
- default value processors
- classmethod validators

By converting all supported forms into a UnionType, the system avoids branching
logic and keeps runtime checks fast and deterministic.

## Anti-optional rule
Optionality (`None`, `NoneType`) is not allowed inside `_type`.  
Absence of value must be modeled at a higher level, not inside the core type
constraint.

## Performance notes
- Atomic types short‑circuit immediately.
- Tuple processing is linear in the number of elements.
- UnionType handling is constant time.
"""