from typing import TYPE_CHECKING
# Outers
from ...._commons.constants import VALUE
# Inners
from .validations import raise_snapshot_incompatible_error
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.alias_typings import SnapshotTuple, NodesTuple, SnapshotDiffTuple


def compare_snapshots(
    nodes_tuple: "NodesTuple",
    snapshot1: "SnapshotTuple",
    snapshot2: "SnapshotTuple",
    *,
    constants_only: bool = False,
) -> "SnapshotDiffTuple":
    """
    Compares two snapshots and returns a tuple of (path, old_value, new_value)
    for all nodes whose values differ. Optionally filters out composite nodes
    when `constants_only=True`.
    """

    diffs = []

    try:
        # 1. Iterate through nodes and both snapshots simultaneously
        for (_, path), snap1_value, snap2_value in zip(nodes_tuple, snapshot1, snapshot2):

            # 2. Skip composite nodes when constants_only=True
            if constants_only and path[-1] == VALUE:
                continue

            # 3. Append differences
            if snap1_value != snap2_value:
                diffs.append((path, snap1_value, snap2_value))

        return tuple(diffs)

    except (ValueError, TypeError) as error:
        raise_snapshot_incompatible_error(
            nodes_tuple=nodes_tuple,
            snapshot1=snapshot1,
            snapshot2=snapshot2,
            error=error,
        )


_DESIGN_NOTES = """
# compare_snapshots

## Purpose
Compares two snapshots and returns a structured list of differences. Each
difference is represented as `(path, old_value, new_value)`, where `path`
identifies the node in the object tree. This function is used by history
tracking, immutability pipelines, debugging tools, and diffing utilities.

## Architectural role
Snapshot comparison is a core operation in the Simple system. It enables:

- detecting changes between two states,
- building history entries,
- validating immutability transitions,
- computing diffs for debugging and serialization,
- determining which nodes require recalculation.

The function relies on `nodes_tuple`, which provides a deterministic structural
representation of the object tree.

## Constants-only mode
When `constants_only=True`, composite nodes (identified by `path[-1] == VALUE`)
are ignored. This mode is used by immutability pipelines where only leaf-level
changes matter.

## Error handling
Snapshot comparison requires both snapshots to:

- be iterable,
- have the same length as `nodes_tuple`,
- contain raw values in the correct order.

If any of these conditions fail, Python raises `ValueError` or `TypeError`.
These are caught and delegated to `raise_snapshot_incompatible_error`, which
provides a structured diagnostic message.

This ensures that invalid snapshots never silently propagate through the system.

## Deterministic behavior
The comparison is deterministic because:

- `nodes_tuple` is stable,
- traversal order is fixed,
- snapshots are positional,
- diff output preserves node order.

This determinism is essential for history tracking and immutability logic.

## Notes
- This function is intentionally minimal and side-effect-free.
- All structural logic is delegated to `nodes_tuple`.
- All error logic is delegated to `raise_snapshot_incompatible_error`.
"""