from typing import TYPE_CHECKING, NoReturn, Any
# Outers
from .....exceptions import SimpleRuntimeError

# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.immutable import ImmutableMethodsProtocol


def raise_with_changes_input_not_dict(
    instance: "ImmutableMethodsProtocol",
    value: Any,
) -> NoReturn:
    """
    Raises an error when the input to `with_changes` is not a dictionary.
    """

    raise SimpleRuntimeError(
        error_name="IMMUTABILITY UPDATE ERROR",
        label="changes_dict",
        expected="A dictionary mapping constant names to new values.",
        value=repr(value),
        problem=(
            "Invalid input provided to `with_changes`.",
            "The method expects a dictionary of constant updates."
        ),
        context=(
            f"Immutable update attempted on instance '{type(instance).__name__}'.",
            f"Provided value type: {type(value).__name__}"
        ),
        how_to_fix=(
            "Ensure that `changes_dict` is a dictionary.",
            "Example: {'width': 10, 'height': 20}",
            "For tuple-based updates, use `with_constants` instead."
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_with_changes_input_not_dict

## Purpose
Raises a structured error when `with_changes` receives a non-dictionary input.

## Why this validation exists
`with_changes` is a convenience wrapper over `with_any`, which expects a tuple
of `(name, value)` pairs.  
To keep the API ergonomic, `with_changes` accepts a dictionary and converts it
to a tuple internally.

If the input is not a dictionary, the conversion cannot be performed safely.

## Execution context
Used inside `ImmutableMethods.with_changes` before delegating to `with_any`.

## Notes
- Pure raise function, no conditional logic.
- Consistent with the immutability validation style.
"""