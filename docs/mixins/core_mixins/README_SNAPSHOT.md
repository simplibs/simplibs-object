from typing import TYPE_CHECKING
# Inners
from .NodesTuple import NodesTuple
from ._utils.snapshot import compare_snapshots
# Annotations
if TYPE_CHECKING:
    from ..._core.protocols.mixins.core_mixins import SnapshotProtocol
    from ..._core.protocols.alias_typings import SnapshotTuple, SnapshotDiffTuple


class Snapshot(NodesTuple):
    """
    Stores complete snapshots of the instance's state and allows
    restoring them. A snapshot is a plain tuple of values in the same
    order as _nodes_tuple.
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Slot definition
    __slots__ = ()

    # ----------------------------------------
    # Methods - BUILD / RESTORE / COMPARE
    # ----------------------------------------

    def _build_snapshot(
        self: "SnapshotProtocol"
    ) -> "SnapshotTuple":
        """Builds a snapshot as a tuple of values according to _nodes_tuple."""
        # noinspection PyProtectedMember
        return tuple(
            instance._value for instance, _
            in self._nodes_tuple
        )

    def _restore_snapshot(
        self: "SnapshotProtocol",
        snapshot: "SnapshotTuple"
    ) -> None:
        """Restores the instance's state from a snapshot."""
        for (instance, _), value in zip(self._nodes_tuple, snapshot):
            instance._value = value

    def _compare_snapshots(
        self: "SnapshotProtocol",
        snapshot1: "SnapshotTuple",
        snapshot2: "SnapshotTuple",
        *,
        constants_only: bool = False
    ) -> "SnapshotDiffTuple":
        """Compares two snapshots."""
        return compare_snapshots(
            self._nodes_tuple,
            snapshot1,
            snapshot2,
            constants_only=constants_only
        )


_DESIGN_NOTES = """
# Snapshot

## Purpose
Gives an instance the ability to capture its entire state as a plain,
inert tuple of values, and later restore or compare against that
captured state. This is the shared foundation behind copying, pickling,
default-state resets, dirty tracking, and undo/redo history — anywhere
the ecosystem needs "what did this look like at some point."

## Compatibility
- No compatibility flags — the three methods are pure data operations
  over `_nodes_tuple`, valid for atoms and composites, mutable and
  immutable alike. Restrictions (e.g. `_mutable_only`) belong to the
  higher-level mixins that *use* this foundation (`DirtyTracking`,
  `DefaultState`), not to `Snapshot` itself.

## Logic
- `_build_snapshot()` walks `_nodes_tuple` and pulls out each node's raw
  `_value`, in the same fixed order — the snapshot is just a tuple of
  values, position-matched to `_nodes_tuple`, nothing more.
- `_restore_snapshot(snapshot)` does the reverse: zips `_nodes_tuple`
  against the given snapshot and writes each value back directly onto
  `instance._value`. This bypasses the normal setter/validation pipeline
  by design — a restore is trusted to already be a value the instance
  previously held.
- `_compare_snapshots(snapshot1, snapshot2, constants_only=...)`
  delegates to the `compare_snapshots` utility, using `_nodes_tuple` to
  translate positional differences back into meaningful `(path, old,
  new)` triples. `constants_only` lets a caller ignore composite-level
  "value" nodes and diff only the leaf constants.

## Notes
- A snapshot is intentionally "dumb" — a bare tuple with no metadata
  about which mixin produced it. Its meaning only exists relative to the
  `_nodes_tuple` it was built from, which is why restore/compare always
  take the *current* instance's `_nodes_tuple` as context.
- `_restore_snapshot` writing straight to `instance._value` (not through
  a public setter) is the same category of deliberate low-level access
  seen elsewhere in the ecosystem (e.g. `validate=False` in internal
  calls) — an architectural choice, not an oversight.
"""
