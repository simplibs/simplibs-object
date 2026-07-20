from typing import TYPE_CHECKING
from types import NoneType, UnionType
from functools import reduce
from operator import or_
from simplibs.sentinels import UNSET
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
# Annotations
if TYPE_CHECKING:
    from ......protocols.classes import SimpleClassLike


def process_type(
    owner_class: "SimpleClassLike",
) -> tuple[type | UnionType, str]:
    """
    Validates the structural integrity of the '_type' attribute and transforms legacy tuples into modern UnionTypes.

    Guarantees that the resulting type constraint contains no explicit None/NoneType references
    and remains fully compatible with runtime isinstance checks and static type hinting signatures.
    """

    # 1. Fetch the raw metadata attribute from the class blueprint
    raw_type = getattr(owner_class, "_type", UNSET)

    # 2. Early structural guards execution
    if raw_type is UNSET or not raw_type:
        validate_type_is_defined(raw_type, owner_class)
        validate_type_is_not_none(raw_type, owner_class)
        validate_type_is_not_empty(raw_type, owner_class)

    # 3. Fast-track processing for atomic type constraints (e.g., _type = int)
    if isinstance(raw_type, type):
        return raw_type, raw_type.__name__

    # 4. Processing for modern native Python Union expressions (e.g., _type = int | str)
    if isinstance(raw_type, UnionType):

        # 4.1 Enforce strict exclusion of optional/absent state indicators
        if NoneType in raw_type.__args__:
            raise_union_type_contain_none(owner_class)

        # 4.2 Return the validated UnionType and its standardized string representation
        return raw_type, str(raw_type)

    # 5. Processing for multi-type collections defined as standard Python tuples (e.g., _type = (int, str))
    if isinstance(raw_type, tuple):

        # 5.1 Iterate through individual collection segments to verify deep structural health
        valid_types = []
        for inner_type in raw_type:

            # 5.1.1 Verify nested layer limits and structural leaf validity
            if isinstance(inner_type, tuple) or inner_type is None:
                validate_type_tuple_is_not_nested(inner_type, raw_type, owner_class)
                validate_type_from_tuple_is_not_none(inner_type, raw_type, owner_class)

            # 5.1.2 Accumulate clean structural component type references
            valid_types.append(inner_type)

        # 5.2 Cast the verified collection sequence into a modern flat UnionType representation
        final_type = reduce(or_, valid_types)
        return final_type, str(final_type)

    # 6. Fallthrough terminal guard execution for completely unrecognized attribute definitions
    raise_validate_type_is_not_valid(raw_type, owner_class)


_DESIGN_NOTES = """
# process_type

## Purpose
Acts as the authoritative architectural gatekeeper for the `_type` configuration attribute across both atomic Constants and composite Objects. It parses disparate type declaration styles (atomic types, native Union expressions, and historical tuples) and normalizes them into a singular, predictable runtime type constraint blueprint.

## The Normalization Strategy
To keep the framework's internal validation engine fast and robust, `process_type` dynamically transforms legacy tuple sequences into modern native Python `UnionType` structures using the binary bitwise OR operator (`reduce(or_, valid_types)`). 

This approach enforces an absolute semantic guarantee:
- Downstream instance validators can execute standard `$isinstance(value, compiled_type)$` checks without complex nested branching logic.
- Type definitions are consistently represented as strings for diagnostic logs and reflection routines.

## Deterministic Processing Stages & Short-Circuit Evaluations


```

[Raw Input: getattr]
│
├──► [UNSET / Falsy Shield] ──► (Missing, None, Empty Collection Guards)
│
├──► [Atomic type Check] ──────► [Fast Return] Return type + **name**
│
├──► [Native UnionType] ───────► Check for NoneType ──► Return Union + str()
│
└──► [Python tuple] ───────────► Loop through elements:
├── Check for sub-tuples (Flatten verification)
└── Check for None literals
Transform: reduce(or_) ──► Return Union + str()
│
└──► [Fallback] ──────────────► Terminal catch-all (raise_validate_type_is_not_valid)

```

## Architectural Design Intentions
- **Strict Anti-Optional Design**: The framework treats data fields as reliable, concrete runtime segments. Allowing embedded `None` or `NoneType` within a type matrix introduces ambiguous runtime execution vectors. By filtering this constraint out early during the boot phase via `raise_union_type_contain_none` and `validate_type_from_tuple_is_not_none`, the architecture guarantees structural stability.
- **Performance Considerations**: Atomic type checks are processed immediately at stage 3. This serves as a fast-track branch since the vast majority of domain primitives utilize single-type bounds. This pattern minimizes processing overhead by completely skipping collection allocations and iterations for basic instances.
"""