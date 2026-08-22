from typing import TYPE_CHECKING, NoReturn
# Outers
from ......exceptions import SimpleRuntimeError
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.core_mixins import SerializationProtocol


def raise_missing_composite_key(
    instance: "SerializationProtocol",
    missing_key: str,
    full_path: tuple[str, ...],
) -> NoReturn:
    """
    Raises an error when a required composite dictionary key is missing
    during state reconstruction.
    """

    raise SimpleRuntimeError(
        error_name="STATE DICT MISSING KEY",
        label="composite key",
        expected=f"Key '{missing_key}' to exist in nested dictionary structure.",
        value=missing_key,
        problem=(
            "A required key is missing in the composite branch of the state dictionary.",
            f"The key '{missing_key}' was expected but not found."
        ),
        context=(
            f"State import attempted on instance '{type(instance).__name__}'.",
            f"Traversal path: {full_path}",
            "Composite nodes must contain all required nested keys."
        ),
        how_to_fix=(
            "Ensure the state dictionary contains all composite keys according to the object's structure.",
            "Use `to_dict()` to generate a correct structure.",
            "Verify that nested dictionaries are complete and not partially missing."
        ),
        exception=KeyError,
    )


_DESIGN_NOTES = """
# raise_missing_composite_key

## Purpose
Raises a structured error when a composite dictionary branch is missing a key
required by the `_nodes_tuple` structural path.

## Why this validation exists
Composite nodes represent nested structures.  
If any key in the path is missing, the object cannot be reconstructed safely.

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