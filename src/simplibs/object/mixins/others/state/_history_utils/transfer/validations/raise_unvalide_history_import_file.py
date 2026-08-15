from typing import TYPE_CHECKING, NoReturn
# Outers
from .......exceptions import SimpleLogicError
# Annotations
if TYPE_CHECKING:
    from ......._core.protocols.mixins.state import HistoryProtocol


def raise_unvalide_history_import_file(
    instance: "HistoryProtocol",
    value: object,
) -> NoReturn:
    """
    Raises an error when the provided history import container is not a dictionary.
    """

    raise SimpleLogicError(
        error_name="HISTORY IMPORT FORMAT ERROR",
        label="history import container",
        expected="A dictionary containing OWNER_CLASS and HISTORY fields.",
        value=type(value).__name__,
        problem=(
            "Invalid history import format.",
            "History import requires a dictionary structure."
        ),
        context=(
            f"History import attempted on instance '{type(instance).__name__}'.",
            f"Provided value type: {type(value).__name__}"
        ),
        how_to_fix=(
            "Ensure the input is a dictionary.",
            "Use `export_history_to_dict()` to generate a valid import structure.",
            "Do not pass lists, tuples, strings, or other unsupported types."
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_unvalide_history_import_file

## Purpose
Raises a structured error when the user attempts to import history from a value
that is not a dictionary.

## Why this validation exists
History import requires a strict dictionary format containing:
- OWNER_CLASS,
- HISTORY,
- optional metadata fields.

Passing anything else (list, tuple, string, None, etc.) would make the import
ambiguous or impossible.

Failing early ensures:
- predictable import behavior,
- safe restoration,
- clear diagnostics.

## Execution context
Used inside `import_history_from_dict` as the first validation step.

## Notes
- Pure raise function, no conditional logic.
- Used exclusively by the History mixin.
"""