from typing import TYPE_CHECKING, NoReturn, Any
# Outers
from .......exceptions import SimpleLogicError
from simplibs.sentinels import UNSET

# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.core_mixins import SerializationProtocol


def raise_unvalid_owner_class_mismatch_for_state_dict(
    instance: "SerializationProtocol",
    got_owner_class: Any,
) -> NoReturn:
    """
    Raises an error when the imported state dictionary belongs to a different
    owner class than the current instance.
    """
    expected_owner_class = instance.meta.owner_class

    raise SimpleLogicError(
        error_name="STATE DICT OWNER CLASS MISMATCH",
        label="owner_class",
        expected=f"Owner class: {expected_owner_class!r}",
        value=repr(got_owner_class),
        problem=(
            "Imported state dictionary belongs to a different class.",
            "State reconstruction requires exact owner class identity."
        ),
        context=(
            f"State import attempted on instance '{type(instance).__name__}'.",
            f"Expected owner class: {expected_owner_class!r}",
            f"Got owner class: {got_owner_class!r}",
            (
                "Note: If the value is UNSET, the dictionary is missing the "
                "required OWNER_CLASS field."
                if got_owner_class is UNSET else ""
            )
        ),
        how_to_fix=(
            "Ensure the dictionary was produced by the same class.",
            "Use `to_dict()` or `export_history_to_dict()` on an instance of the correct type.",
            "Do not mix state dictionaries between different component classes.",
            "Verify that OWNER_CLASS is present and correct in the input dictionary."
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_unvalid_owner_class_mismatch_for_state_dict

## Purpose
Raises a structured error when the user attempts to reconstruct instance state
from a dictionary that belongs to a different owner class.

## Why this validation exists
State dictionaries encode structural metadata tied to the component class.
Importing state from a different class would cause:

- corrupted internal structure,
- invalid node traversal,
- mismatched VALUE fields,
- unpredictable behavior.

Failing early ensures:
- structural safety,
- deterministic behavior,
- clear diagnostics.

## Execution context
Used inside `from_dict` immediately after validating the input container.

## Notes
- Pure raise function, no conditional logic.
- Used exclusively by the Serialization mixin.
"""