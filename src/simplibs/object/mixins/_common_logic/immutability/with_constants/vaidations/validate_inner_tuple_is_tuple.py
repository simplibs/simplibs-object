from typing import TYPE_CHECKING, NoReturn
# Outers
from ......exceptions import SimpleLogicError
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.core_mixins import InfrastructureProtocol


def validate_inner_tuple_is_tuple(
    instance: "InfrastructureProtocol",
    inner_tuple: object,
) -> None:
    """
    Validates that the provided inner_tuple is actually a tuple.
    """

    if isinstance(inner_tuple, tuple):
        return

    raise SimpleLogicError(
        error_name="IMMUTABILITY BATCH UPDATE ERROR",
        label="change item",
        expected="Each change must be a tuple: (name, value).",
        value=type(inner_tuple).__name__,
        problem=(
            "Invalid structure for change item. ",
            "Batch immutable update requires each item to be a tuple."
        ),
        context=(
            f"Batch update attempted on instance '{type(instance).__name__}'. ",
            "The provided item is not a tuple."
        ),
        how_to_fix=(
            "Ensure each change is provided as a tuple: (name, value).",
            "Example: ('age', 42)",
            "Do not use lists, dicts, or other container types.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# validate_inner_tuple_is_tuple

## Purpose
Ensures that each item inside a batch update (`with_constants`, `with_any`) is
actually a tuple.  
Batch updates rely on tuple-based structures for deterministic ordering,
structural validation, and predictable unpacking.

If an item is not a tuple, the update cannot be interpreted safely.

## Architectural reasoning
The immutability pipeline expects:

- `(name, value)` for single updates,
- `((name, value), (name, value), ...)` for batch updates.

Using tuples guarantees:

- stable ordering,
- simple structural validation,
- predictable unpacking,
- no accidental key/value inversion (as with dicts),
- no ambiguity (as with lists).

If the item is not a tuple:

- the pipeline cannot determine the intended structure,
- composite/constant routing becomes impossible,
- debugging becomes significantly harder.

Therefore, the function fails early with a clear diagnostic error.

## Pipeline position
This validation is part of step **4.3.1** in `with_constants`:

1. Check if `inner_tuple` is a tuple.  
2. If not → raise this error immediately.  
3. No further validation is performed on this item.

This ensures that only structurally valid items enter deeper validation layers.

## Diagnostic value
The error message provides:

- the invalid type,
- the expected structure,
- the context of the batch update,
- actionable steps to fix the issue.

This makes the error friendly, actionable, and easy to understand.

## Notes
- This is a pure validation function: it performs no additional logic.
- It is used by both `with_constants` and `with_any`.
- All batch update items must pass this check before further validation.

"""