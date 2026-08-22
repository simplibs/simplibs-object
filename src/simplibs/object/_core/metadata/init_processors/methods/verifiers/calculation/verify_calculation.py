from typing import Any, TYPE_CHECKING
from types import UnionType
from simplibs.sentinels import UNSET
# Inners
from .decompose_method import verify_decompose_outcome
from .validations import (
    raise_method_raised_exceptions,
    raise_method_return_unvalide_outcome_type,
)
# Annotations
if TYPE_CHECKING:
    from ......protocols.classes import SimpleClassLike
    from ......protocols.methods import ClassMethodProtocol


def verify_calculation(
    bound_method: "ClassMethodProtocol",
    test_value: Any,
    expected_return_type: type | UnionType,
    owner_class: "SimpleClassLike",
) -> Any:
    """Executes a dry-run of the method and validates its return type and structure."""

    if bound_method is UNSET:
        return UNSET

    # 1. Initialize result placeholder
    calculate_result = UNSET

    # 2. Execute dry-run and intercept exceptions
    try:
        calculate_result = bound_method(*test_value)
    except Exception as e:
        raise_method_raised_exceptions(e, bound_method)

    # 3. Validate return type
    if not isinstance(calculate_result, expected_return_type):
        raise_method_return_unvalide_outcome_type(
            calculate_result,
            expected_return_type,
            bound_method,
        )

    # 4. Special validation for '_decompose'
    if bound_method.__func__.__name__ == "_decompose":
        # noinspection PyTypeChecker
        verify_decompose_outcome(
            calculate_result,
            owner_class,
            bound_method,
        )

    # 5. Return verified result
    return calculate_result



_DESIGN_NOTES = """
# verify_calculation

## Purpose
Runs a controlled dry-run of a classmethod to ensure:
- it executes without raising exceptions,
- it returns a value of the expected type,
- and for `_decompose`, the returned tuple matches the structural metadata.

## Behavior

### 1. Dry-run execution
The method is invoked with `*test_value`.  
Any exception is intercepted and repackaged via `raise_method_raised_exceptions`.

### 2. Type validation
The result is checked using `isinstance` against the expected return type.  
If invalid, `raise_method_return_unvalide_outcome_type` is triggered.

### 3. Decompose-specific validation
If the method is `_decompose`, the result is passed to `verify_decompose_outcome`,
which validates:
- tuple length,
- item types,
- item default values.

### 4. Verified output
If all checks pass, the result is returned unchanged.

## Notes
This orchestrator is the final operational validation step in the method pipeline.
"""