from typing import TYPE_CHECKING, NoReturn, Any
# Outers
from .......exceptions import SimpleRuntimeError
# Annotations
if TYPE_CHECKING:
    from ......._core.protocols.mixins.state import HistoryProtocol


def raise_unvalide_owner_class_mismatch(
    instance: "HistoryProtocol",
    got_owner_class: Any,
) -> NoReturn:
    """
    Raises an error when the imported history belongs to a different owner class.
    """
    expected_owner_class = instance.meta.owner_class

    raise SimpleRuntimeError(
        error_name="HISTORY OWNER CLASS MISMATCH",
        label="owner_class",
        expected=f"Owner class: {expected_owner_class}",
        value=repr(got_owner_class),
        problem=(
            "Imported history belongs to a different class.",
            "History snapshots must originate from the same component type."
        ),
        context=(
            f"History import attempted on instance '{type(instance).__name__}'.",
            f"Expected owner class: {expected_owner_class}",
            f"Got owner class: {got_owner_class!r}"
        ),
        how_to_fix=(
            "Ensure the imported dictionary was produced by the same class.",
            "Use `export_history_to_dict()` on an instance of the correct type.",
            "Do not mix histories between different components."
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_unvalide_owner_class_mismatch

## Purpose
Raises a structured error when the user attempts to import history from a
different component class.

## Why this validation exists
Snapshots encode structural metadata tied to the component class.  
Importing history from a different class would cause:

- corrupted state,
- invalid snapshot restoration,
- mismatched node ordering,
- unpredictable behavior.

Failing early ensures:
- structural safety,
- deterministic behavior,
- clear diagnostics.

## Execution context
Used inside `import_history_from_dict` immediately after validating the input
container.

## Notes
- Pure raise function, no conditional logic.
- Used exclusively by the History mixin.
"""