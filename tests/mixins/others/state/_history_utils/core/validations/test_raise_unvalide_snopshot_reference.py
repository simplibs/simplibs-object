from typing import TYPE_CHECKING, NoReturn
from datetime import datetime
# Outers
from ......exceptions import SimpleMixinError
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.state import HistoryProtocol


def raise_unvalide_snopshot_reference(
    instance: "HistoryProtocol",
    ref: object,
) -> NoReturn:
    """
    Raises an error when the provided snapshot reference is neither an integer
    nor a datetime object.
    """

    raise SimpleMixinError(
        error_name="HISTORY SNAPSHOT REFERENCE ERROR",
        label="snapshot reference",
        expected="Either an integer index or a datetime timestamp.",
        value=type(ref).__name__,
        problem=(
            "Invalid snapshot reference provided.",
            "Snapshot lookup requires either an integer index or a datetime timestamp."
        ),
        context=(
            f"History lookup attempted on instance '{type(instance).__name__}'.",
            f"Provided value type: {type(ref).__name__}"
        ),
        how_to_fix=(
            "Use an integer index to reference snapshots by position.",
            "Use a datetime value to reference snapshots by timestamp.",
            "Do not pass strings, floats, None, or other unsupported types."
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_unvalide_snopshot_reference

## Purpose
Raises a structured error when the user provides a snapshot reference that is
neither an integer nor a datetime object.

## Why this validation exists
Snapshot lookup supports exactly two reference modes:
- index-based lookup (`int`),
- timestamp-based lookup (`datetime`).

Any other type would make the lookup ambiguous or meaningless.

Failing early ensures:
- predictable navigation,
- clear diagnostics,
- safe snapshot restoration.

## Execution context
Used inside `find_snapshot` when the reference does not match any supported
type. It is the final validation step before rejecting the input.

## Notes
- Pure raise function, no conditional logic.
- Used exclusively by the History mixin.
"""