from typing import TYPE_CHECKING, NoReturn
# Outers
from ......exceptions import SimpleRuntimeError

# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.core_mixins import SerializationProtocol


def raise_unvalid_state_dict_input(
    instance: "SerializationProtocol",
    value: object,
) -> NoReturn:
    """
    Raises an error when the provided state dictionary is not a valid dict.
    """

    raise SimpleRuntimeError(
        error_name="STATE DICT INPUT ERROR",
        label="state dictionary",
        expected="A dictionary mapping node paths to values.",
        value=repr(value),
        problem=(
            "Invalid input provided for state reconstruction.",
            "State import requires a dictionary structure."
        ),
        context=(
            f"State import attempted on instance '{type(instance).__name__}'.",
            f"Provided value type: {type(value).__name__}"
        ),
        how_to_fix=(
            "Ensure the input is a dictionary.",
            "Use `to_dict()` or `export_history_to_dict()` to generate valid structures.",
            "Do not pass lists, tuples, strings, or other unsupported types."
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_unvalid_state_dict_input

## Purpose
Raises a structured error when the user attempts to reconstruct instance state
from a value that is not a dictionary.

## Why this validation exists
The `from_dict` pipeline requires a strict dictionary format containing:
- OWNER_CLASS,
- nested composite structures,
- VALUE fields for atomic nodes.

Passing anything else (list, tuple, string, None, etc.) would make the import
ambiguous or impossible.

Failing early ensures:
- predictable import behavior,
- safe restoration,
- clear diagnostics.

## Execution context
Used inside `from_dict` as the first validation step.

## Notes
- Pure raise function, no conditional logic.
- Used exclusively by the Serialization mixin.
"""