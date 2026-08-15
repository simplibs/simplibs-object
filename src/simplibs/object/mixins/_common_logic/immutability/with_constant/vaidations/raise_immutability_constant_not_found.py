from typing import TYPE_CHECKING, NoReturn
# Outers
from ......exceptions import SimpleLogicError
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.core_mixins import InfrastructureProtocol


def raise_immutability_constant_not_found(
    instance: "InfrastructureProtocol",
    name: str,
) -> NoReturn:
    """
    Raises an error when a constant name is not found in the instance's
    `_constant_names_set` during an immutable update.
    """

    # noinspection PyProtectedMember
    raise SimpleLogicError(
        error_name="IMMUTABILITY UPDATE ERROR",
        label="constant name",
        expected="Name must refer to a valid constant defined in the instance.",
        value=name,
        problem=(
            f"Constant '{name}' does not exist in the instance. ",
            "Immutable update cannot be applied."
        ),
        context=(
            f"Immutable update attempted on instance '{type(instance).__name__}'. ",
            f"Valid constants: {instance._constant_names_set}"
        ),
        how_to_fix=(
            "Ensure that the provided name refers to a valid constant.",
            "Check the instance's `_constant_names_set` for available constants.",
            "If the name is meant to be a composite, use `with_composite` instead.",
        ),
        exception=KeyError,
    )


_DESIGN_NOTES = """
# raise_immutability_constant_not_found

## Purpose
Ensures that immutable updates targeting constants are always applied to valid,
existing constant nodes.  
If a user attempts to update a constant that does not exist, this function
raises a structured diagnostic error explaining exactly what went wrong and how
to fix it.

This protects the immutability pipeline from invalid structural updates.

## Architectural reasoning
Immutable updates rely on strict structural correctness:

- constants must exist,
- constants must be addressable via `_constant_names_set`,
- constants must have valid metadata and validation logic.

If a constant name is invalid:

- the update cannot be applied,
- composite recalculation would be incorrect,
- snapshot reconstruction would be inconsistent,
- debugging would become significantly harder.

This raise function ensures that the pipeline fails early, clearly, and safely.

## Pipeline position
This function is used in the very first validation step of `with_constant`:

1. Check whether `name` is in `_constant_names_set`.
2. If not → raise this error immediately.
3. No further processing is performed.

This guarantees that invalid updates never reach deeper pipeline layers.

## Diagnostic value
The error message provides:

- the invalid constant name,
- the list of valid constants,
- the context of the attempted update,
- actionable steps to fix the issue,
- a clear distinction between constants and composites.

This makes the error friendly, actionable, and easy to understand.

## Notes
- This is a pure `raise_...` function: it performs no conditional logic.
- It is used exclusively by the immutability update pipeline.
- All immutable constant updates must pass this check.
"""