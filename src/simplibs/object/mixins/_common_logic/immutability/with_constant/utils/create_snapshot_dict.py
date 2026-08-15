from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.alias_typings import NodesTuple, SnapshotDict


def create_snapshot_dict(
    nodes_tuple: "NodesTuple",
) -> "SnapshotDict":
    """
    Creates a dictionary-based snapshot of the current instance state,
    using snake_case names as keys.
    """

    # 1. Build snapshot dictionary
    # noinspection PyProtectedMember
    return {
        instance.meta.name_snake: instance._value
        for instance, _ in nodes_tuple
    }


_DESIGN_NOTES = """
# create_snapshot_dict

## Purpose
Creates a lightweight dictionary snapshot of the current instance state.
Each entry maps a node’s `name_snake` identifier to its raw `_value`. This
snapshot is used as an intermediate representation in immutability pipelines,
serialization, debugging, and composite recalculation.

## Architectural role
This function is a foundational utility for:

- `with_constant`, `with_constants`, `with_composite`
- snapshot-based reconstruction (`create_new_instance`)
- composite recalculation (`reacalculate_owner_value`)
- serialization pipelines (`to_dict`, `from_dict`)
- debugging and diffing tools

It provides a simple, flat, deterministic representation of the instance’s
current values.

## Why dictionary form is needed
While `SnapshotMixin` uses tuple-based snapshots for immutability and
restoration, dictionary snapshots are more convenient for:

- targeted updates,
- merging changes,
- recalculating composite values,
- mapping names to values,
- building new tuple snapshots.

The dictionary form allows constant and composite updates to be expressed
cleanly and efficiently.

## Deterministic behavior
The snapshot dictionary:

- preserves the order of `nodes_tuple` (via iteration),
- uses stable `name_snake` identifiers,
- contains only raw values (no nested structures),
- is safe for merging and transformation.

This determinism is essential for immutability pipelines.

## Stability guarantee
Any change to this function would affect:

- immutability behavior,
- composite recalculation,
- serialization consistency,
- snapshot reconstruction,
- debugging tools.

Therefore, `create_snapshot_dict` is treated as a **core invariant** of the
immutability subsystem.

## Notes
- This function is intentionally minimal and side-effect-free.
- It is not part of the public API; it is used internally by mixins.
- All structural logic is delegated to `nodes_tuple`.
"""