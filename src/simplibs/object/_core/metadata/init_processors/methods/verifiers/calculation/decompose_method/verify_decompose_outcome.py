from typing import Any, TYPE_CHECKING
# Inners
from .validations import (
    raise_decompose_unvalide_outcome_length,
    validate_decompose_unvalide_item_type,
    validate_decompose_unvalide_item_value,
)
# Annotations
if TYPE_CHECKING:
    from .......protocols.methods import ClassMethodProtocol
    from .......protocols.classes import SimpleClassLike


def verify_decompose_outcome(
    calculate_default: tuple[Any, ...],
    owner_class: "SimpleClassLike",
    bound_method: "ClassMethodProtocol",
) -> None:
    """Verifies structural correctness of the tuple returned by '_decompose'."""

    # 1. Extract inner metadata
    # noinspection PyProtectedMember
    inners = owner_class._inners

    # 2. Validate tuple length
    if len(calculate_default) != len(inners):
        raise_decompose_unvalide_outcome_length(
            calculate_default,
            inners,
            bound_method,
        )
        return

    # 3. Validate each item
    for index, inner in enumerate(inners):
        value = calculate_default[index]
        expected_type = inner.meta.value_type

        # 3.1 Type or default mismatch → run micro-validations
        if not isinstance(value, expected_type) and value != inner.meta.default:
            validate_decompose_unvalide_item_type(
                value,
                expected_type,
                inner,
                inners,
                bound_method,
            )
            validate_decompose_unvalide_item_value(
                value,
                inner,
                inners,
                bound_method,
            )



_DESIGN_NOTES = """
# verify_decompose_outcome

## Purpose
Ensures that the tuple returned by `_decompose` matches the structural metadata
defined in `owner_class.meta.inners`.

## Behavior

### 1. Metadata extraction
The function retrieves the list of inner components (`_inners`) from the class
metadata.

### 2. Length validation
Before checking individual items, the function verifies that the returned tuple
has the same number of elements as `_inners`.  
If not, it delegates to `raise_decompose_unvalide_outcome_length`.

### 3. Item validation
For each item:
- It checks whether the value is either:
  - an instance of the expected type, or  
  - equal to the default sentinel value.
- If both checks fail, it delegates to:
  - `validate_decompose_unvalide_item_type`
  - `validate_decompose_unvalide_item_value`

## Notes
This orchestrator is used exclusively inside `verify_calculation` when the
method being validated is `_decompose`.
"""