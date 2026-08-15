from typing import TYPE_CHECKING, NoReturn
# Outers
from ......exceptions import SimpleMixinError
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.core_mixins import InfrastructureProtocol
    from ......_core.protocols.alias_typings import ChangeTuple, ChangesTuple


def raise_immutability_constants_changes_not_tuple(
    instance: "InfrastructureProtocol",
    changes: "ChangeTuple | ChangesTuple | None",
) -> NoReturn:
    """
    Raises an error when the `changes` argument passed to `with_constants`
    is not a tuple.
    """

    raise SimpleMixinError(
        error_name="IMMUTABILITY UPDATE ERROR",
        label="changes",
        expected="Tuple of (name, value) pairs or a single (name, value) tuple.",
        value=type(changes).__name__ if changes is not None else "None",
        problem=(
            "Invalid type for `changes` argument in `with_constants`. ",
            "Immutable batch update requires a tuple-based structure."
        ),
        context=(
            f"Immutable constant batch update on instance '{type(instance).__name__}'. ",
            "The `changes` parameter must be a tuple."
        ),
        how_to_fix=(
            "Pass changes as a tuple: ((name, value), (name, value), ...).",
            "For a single change, use: (name, value) — it will be normalized internally.",
            "Do not use lists, dicts, or other container types for `changes`.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_immutability_constants_changes_not_tuple

## Purpose
Ensures that the `changes` argument passed to `with_constants` has the correct
tuple-based structure.  
The immutability pipeline relies on tuples for deterministic ordering and
structural validation. Any other container type would break these guarantees.

## Architectural reasoning
`with_constants` expects:

- either a single `(name, value)` tuple,
- or a tuple of `(name, value)` tuples.

This design:

- preserves ordering,
- simplifies validation,
- avoids ambiguity of dicts/lists,
- keeps the API minimal and predictable.

If `changes` is not a tuple:

- the pipeline cannot reliably interpret the update,
- structural validation becomes ambiguous,
- debugging and logging lose determinism.

Therefore, the function fails early with a clear, structured error.

## Pipeline position
This function is used at the beginning of the `with_constants` update flow:

1. Check `isinstance(changes, tuple)`.
2. If false → raise this error.
3. No further processing is performed.

This guarantees that only well-formed inputs enter the deeper pipeline.

## Diagnostic value
The error message explains:

- what type was received,
- what structure is expected,
- in which context the error occurred,
- how to fix the issue (including examples).

This makes the error actionable and easy to understand.

## Notes
- This is a pure `raise_...` function: it performs no conditional logic.
- It is used exclusively by the `with_constants` pipeline.
- All batch constant updates must pass this check.
"""