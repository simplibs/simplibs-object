from typing import TYPE_CHECKING, NoReturn, Any
# Outers
from ......exceptions import SimpleMixinError
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.core_mixins import SerializationProtocol


def raise_invalid_composite_structure(
    instance: "SerializationProtocol",
    key: str,
    value: Any,
    full_path: tuple[str, ...],
) -> NoReturn:
    """
    Raises an error when a composite dictionary branch contains an invalid
    structure (expected a dictionary, got something else).
    """

    raise SimpleMixinError(
        error_name="STATE DICT INVALID COMPOSITE STRUCTURE",
        label="composite structure",
        expected=f"A dictionary at key '{key}'.",
        value=repr(value),
        problem=(
            "Invalid structure encountered in composite branch.",
            f"Expected a dictionary at key '{key}', but got {type(value).__name__}."
        ),
        context=(
            f"State import attempted on instance '{type(instance).__name__}'.",
            f"Traversal path: {full_path}",
            "Composite nodes must be represented as nested dictionaries."
        ),
        how_to_fix=(
            "Ensure that all composite branches in the state dictionary are dictionaries.",
            "Use `to_dict()` to generate a correct nested structure.",
            "Verify that no composite node was replaced by a scalar or list."
        ),
        exception=KeyError,
    )


_DESIGN_NOTES = """
# raise_invalid_composite_structure

## Purpose
Raises a structured error when a composite dictionary branch contains a value
that is not a dictionary, even though the structural path requires one.

## Why this validation exists
Composite nodes represent nested structures.  
If any branch is not a dictionary, the object cannot be reconstructed safely.

Failing early ensures:
- structural correctness,
- predictable deserialization,
- clear diagnostics.

## Execution context
Used inside `from_dict` during traversal of nested composite dictionaries.

## Notes
- Pure raise function, no conditional logic.
- Used exclusively by the Serialization mixin.
"""