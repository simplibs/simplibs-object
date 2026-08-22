from typing import TYPE_CHECKING, NoReturn
# Outers
from ......exceptions import SimpleRuntimeError
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.core_mixins import InfrastructureProtocol


def validate_inner_tuple_has_length_two(
    instance: "InfrastructureProtocol",
    inner_tuple: object,
) -> None:
    """
    Validates that the provided inner_tuple has exactly two items:
    (name, value).
    """

    if isinstance(inner_tuple, tuple) and len(inner_tuple) == 2:
        return

    raise SimpleRuntimeError(
        error_name="IMMUTABILITY BATCH UPDATE ERROR",
        label="change item length",
        expected="Tuple of exactly two items: (name, value).",
        value=f"length={len(inner_tuple)}" if isinstance(inner_tuple, tuple) else "not a tuple",
        problem=(
            "Invalid structure for change item. ",
            "Each change must be a 2‑item tuple representing (name, value)."
        ),
        context=(
            f"Batch update attempted on instance '{type(instance).__name__}'. ",
            "The provided tuple does not have exactly two items."
        ),
        how_to_fix=(
            "Ensure each change is provided as a 2‑item tuple.",
            "Correct format: (name, value)",
            "Incorrect formats include: (name,), (name, value, extra), or any other size.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# validate_inner_tuple_has_length_two

## Purpose
Ensures that each change item inside a batch update has exactly two elements:
`(name, value)`.  
This is the minimal structural requirement for immutable updates — without it,
the pipeline cannot determine what should be updated or how.

## Architectural reasoning
The immutability pipeline relies on strict tuple structure:

- index `0` → the node name,
- index `1` → the new value.

If the tuple has a different length:

- unpacking becomes ambiguous,
- routing logic cannot determine whether the item is a constant or composite,
- validation cannot proceed,
- debugging becomes significantly harder.

Failing early prevents structural corruption.

## Pipeline position
This validation is part of step **4.3.1** in `with_constants`:

1. Check that `inner_tuple` has length 2.  
2. If not → raise this error immediately.  
3. No further validation is performed on this item.

This ensures that only structurally correct items enter deeper validation layers.

## Diagnostic value
The error message provides:

- the actual tuple length,
- the expected structure,
- the context of the batch update,
- actionable steps to fix the issue.

This makes the error friendly, actionable, and easy to understand.

## Notes
- This is a pure validation function: it performs no additional logic.
- It is used by both `with_constants` and `with_any`.
- All batch update items must pass this check before further validation.

"""