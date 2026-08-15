from typing import TYPE_CHECKING, NoReturn
# Outers
from ......exceptions import SimpleMixinError
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.alias_typings import SnapshotTuple, NodesTuple


def raise_snapshot_incompatible_error(
    nodes_tuple: "NodesTuple",
    snapshot1: "SnapshotTuple",
    snapshot2: "SnapshotTuple",
    error: Exception,
) -> NoReturn:
    """
    Raises a structured error when two snapshots cannot be compared due to
    incompatible structure, length, or types.
    """

    raise SimpleMixinError(
        error_name="SNAPSHOT COMPARISON ERROR",
        label="Incompatible snapshots",
        expected=(
            "Both snapshots must be iterable and must contain values matching "
            "the length and structure of nodes_tuple."
        ),
        value=(snapshot1, snapshot2),
        problem=(
            "The provided snapshots cannot be compared because their structure "
            "does not match the expected node layout.",
            f"Underlying error: {type(error).__name__}: {error}",
        ),
        context="Snapshot comparison",
        how_to_fix=(
            "Ensure both snapshots were created using the same instance structure.",
            "Verify that both snapshots have the same length as nodes_tuple.",
            "Ensure snapshots contain only raw values, not nested structures.",
            "If the instance structure changed, rebuild snapshots before comparing.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_snapshot_incompatible_error

## Purpose
Raises a structured diagnostic error when two snapshots cannot be compared.
Snapshot comparison requires both snapshots to match the structure, length,
and ordering of `nodes_tuple`. Any deviation makes the comparison invalid.

This error consolidates all structural issues into a single, clear message.

## Why this error exists
Snapshot comparison is a core operation used by:

- history tracking,
- immutability pipelines,
- diffing logic,
- debugging tools.

If snapshots are malformed or incompatible, the system must fail fast with a
clear explanation. Python’s native `ValueError` and `TypeError` provide no
context, so a structured error is required.

## What incompatibility means
Snapshots are incompatible when:

- they have different lengths,
- they do not match the number of nodes,
- they contain non-iterable values,
- they contain nested structures,
- they were created from different instance shapes,
- the instance structure changed after snapshot creation.

## Architectural reasoning
Snapshot comparison is deterministic only when:

- `nodes_tuple` is stable,
- snapshot length matches node count,
- snapshot values correspond to node order.

This error ensures that invalid snapshots never silently propagate through
immutability or history pipelines.

## Diagnostic value
The error reports:

- both snapshots,
- the underlying Python exception,
- expected structure,
- actionable steps to fix the issue.

This makes debugging fast and predictable.

## Notes
- This is a pure `raise_...` function.
- It is used exclusively by snapshot comparison logic.
- All snapshot comparison failures funnel through this error.

"""