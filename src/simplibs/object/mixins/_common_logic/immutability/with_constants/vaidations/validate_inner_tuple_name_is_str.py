from typing import TYPE_CHECKING, NoReturn
# Outers
from ......exceptions import SimpleRuntimeError
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.core_mixins import InfrastructureProtocol


def validate_inner_tuple_name_is_str(
    instance: "InfrastructureProtocol",
    inner_tuple: object,
) -> None:
    """
    Validates that the first element of inner_tuple (the name) is a string.
    """

    if isinstance(inner_tuple, tuple) and isinstance(inner_tuple[0], str):
        return

    raise SimpleRuntimeError(
        error_name="IMMUTABILITY BATCH UPDATE ERROR",
        label="change item name",
        expected="First element of tuple must be a string representing the node name.",
        value=inner_tuple[0] if isinstance(inner_tuple, tuple) else inner_tuple,
        problem=(
            "Invalid structure for change item. ",
            "The first element of each (name, value) tuple must be a string."
        ),
        context=(
            f"Batch update attempted on instance '{type(instance).__name__}'. ",
            "The provided tuple has a non-string name element."
        ),
        how_to_fix=(
            "Ensure the first element of each tuple is a string.",
            "Correct format: ('age', 42)",
            "Incorrect formats include: (123, 42), (None, 42), (object, 42).",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# validate_inner_tuple_name_is_str

## Purpose
Ensures that the first element of each change tuple is a string representing the
node name.  
Immutable updates rely on string-based names to route updates to constants or
composites. Any other type would make routing impossible.

## Architectural reasoning
The immutability pipeline expects:

- `inner_tuple[0]` → node name (string),
- `inner_tuple[1]` → new value.

If the name is not a string:

- routing logic cannot determine whether the update targets a constant or composite,
- metadata lookup fails,
- validation cannot proceed,
- debugging becomes significantly harder.

Failing early prevents structural corruption.

## Pipeline position
This validation is part of step **4.3.1** in `with_constants`:

1. Check that `inner_tuple[0]` is a string.  
2. If not → raise this error immediately.  
3. No further validation is performed on this item.

This ensures that only structurally correct items enter deeper validation layers.

## Diagnostic value
The error message provides:

- the invalid name value,
- the expected type,
- the context of the batch update,
- actionable steps to fix the issue.

This makes the error friendly, actionable, and easy to understand.

## Notes
- This is a pure validation function: it performs no additional logic.
- It is used by both `with_constants` and `with_any`.
- All batch update items must pass this check before further validation.

"""