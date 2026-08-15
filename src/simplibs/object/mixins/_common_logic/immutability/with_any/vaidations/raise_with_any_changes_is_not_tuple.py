from typing import TYPE_CHECKING, NoReturn
# Outers
from ......exceptions import SimpleLogicError
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.core_mixins import InfrastructureProtocol


def raise_with_any_changes_is_not_tuple(
    instance: "InfrastructureProtocol",
    changes: object,
) -> NoReturn:
    """
    Raises an error when the `changes` argument passed to with_any
    is not a tuple.
    """

    raise SimpleLogicError(
        error_name="IMMUTABILITY UPDATE ERROR",
        label="changes",
        expected="Tuple of (name, value) pairs or a single (name, value) tuple.",
        value=type(changes).__name__,
        problem=(
            "Invalid type for `changes` argument in with_any.",
            "Mixed immutable update requires a tuple-based structure."
        ),
        context=(
            f"Mixed update attempted on instance '{type(instance).__name__}'.",
            "The provided `changes` value is not a tuple."
        ),
        how_to_fix=(
            "Pass changes as a tuple: ((name, value), (name, value), ...).",
            "For a single change, use: (name, value).",
            "Do not use lists, dicts, or other container types."
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_with_any_changes_is_not_tuple

## Purpose
Raises a structured error when `with_any` receives a non‑tuple input.  
Mixed updates rely on tuple-based structures for deterministic ordering and
safe routing between constants and composites.

## Why this validation exists
`with_any` accepts either:

- a single `(name, value)` tuple, or  
- a tuple of `(name, value)` tuples.

Other container types cannot be interpreted safely and would break the update
pipeline.

## Execution context
This raise function is used directly inside `with_any` when the input type
check fails.  
It prevents invalid update formats from entering deeper structural logic.

## Notes
- Pure raise function, no conditional logic.
- Used exclusively by the immutability pipeline.
"""