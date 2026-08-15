from typing import Any, TYPE_CHECKING
from types import UnionType
from simplibs.sentinels import UNSET
# Inners
from .validations import (
    validate_default_matches_annotation,
    validate_default_is_defined,
)
# Annotations
if TYPE_CHECKING:
    from ....protocols.classes import SimpleClassLike


def process_default_for_constant(
    default_type: type | UnionType,
    owner_class: "SimpleClassLike",
) -> Any:
    """Validates and returns the '_default' value for a constant."""

    # 1. Fetch raw default
    raw_default = getattr(owner_class, "_default", UNSET)

    # 2. Validate presence and type
    if raw_default is UNSET or not isinstance(raw_default, default_type):
        validate_default_is_defined(raw_default, owner_class)
        validate_default_matches_annotation(raw_default, default_type, owner_class)

    # 3. Return validated default
    return raw_default



_DESIGN_NOTES = """
# process_default_for_constant

## Purpose
Ensures that a constant (`SimpleConstant`) defines a valid `_default` value.
The default must:

- exist,
- and match the type declared in `_type`.

Constants have no inner structure, so the default value defines their runtime identity.

## Pipeline overview

1. **Fetch `_default`**
   Uses `getattr(..., UNSET)` to detect absence reliably.

2. **Validate**
   - `validate_default_is_defined` checks presence.
   - `validate_default_matches_annotation` checks type.

3. **Return**
   Returns the validated default value.

## Why this processor exists
Constants require a concrete baseline value.  
Compositions (`SimpleObject`) compute their value dynamically via `_logic`, so they
must not define `_default`.  
This processor enforces the constant‑only rule.

## Short‑circuit behavior
If `_default` exists and matches the type, the function returns immediately without
running any validation.  
This keeps initialization fast for the common case.

## Upstream dependency
The `default_type` argument must come from `process_type`, which guarantees that
the type is safe for `isinstance` checks.
"""