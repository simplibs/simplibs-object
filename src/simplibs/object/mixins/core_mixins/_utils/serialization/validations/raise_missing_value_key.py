from typing import TYPE_CHECKING, NoReturn
# Outers
from .......exceptions import SimpleLogicError
from simplibs.sentinels import UNSET

# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.core_mixins import SerializationProtocol


def raise_missing_value_key(
    instance: "SerializationProtocol",
    missing_key: str,
    full_path: tuple[str, ...],
) -> NoReturn:
    """
    Raises an error when a required value key is missing in the state dictionary
    during reconstruction.
    """

    raise SimpleLogicError(
        error_name="STATE DICT MISSING VALUE KEY",
        label="value key",
        expected=f"Key '{missing_key}' to exist in the dictionary.",
        value=missing_key,
        problem=(
            "A required value key is missing in the state dictionary.",
            f"The key '{missing_key}' was expected but not found."
        ),
        context=(
            f"State import attempted on instance '{type(instance).__name__}'.",
            f"Traversal path: {full_path}",
            "Atomic VALUE nodes must contain their final key."
        ),
        how_to_fix=(
            "Ensure the state dictionary contains all required VALUE keys.",
            "Use `to_dict()` to generate a correct structure.",
            "Verify that no VALUE field is missing or removed."
        ),
        exception=KeyError,
    )


_DESIGN_NOTES = """
# raise_missing_value_key

## Purpose
Raises a structured error when the final key of a composite path (the VALUE key)
is missing in the state dictionary.

## Why this validation exists
Every atomic node must have a final VALUE key.  
If it is missing, the object cannot be reconstructed safely.

Failing early ensures:
- structural correctness,
- predictable deserialization,
- clear diagnostics.

## Execution context
Used inside `from_dict` during the final step of composite traversal.

## Notes
- Pure raise function, no conditional logic.
- Used exclusively by the Serialization mixin.
"""