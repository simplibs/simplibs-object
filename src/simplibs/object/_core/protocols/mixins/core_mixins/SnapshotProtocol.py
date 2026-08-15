from typing import Protocol, runtime_checkable, TYPE_CHECKING
# Inners
from .NodesTupleProtocol import NodesTupleProtocol
# Annotations
if TYPE_CHECKING:
    from ...alias_typings import SnapshotTuple, SnapshotDiffTuple


@runtime_checkable
class SnapshotProtocol(
    NodesTupleProtocol,
    Protocol
):
    """
    Protocol for the Snapshot mixin.

    Defines the interface for creating, restoring, and comparing complete
    state snapshots across the entire element hierarchy.
    """

    # The mixin has no custom slots/attributes; we only define methods.

    def _build_snapshot(self) -> "SnapshotTuple":
        """Creates and returns a snapshot as a pure tuple of values for all sub-node elements."""
        ...

    def _restore_snapshot(self, snapshot: "SnapshotTuple") -> None:
        """Restores the internal state of all sub-node elements from the provided snapshot."""
        ...

    def _compare_snapshots(
        self,
        snapshot1: "SnapshotTuple",
        snapshot2: "SnapshotTuple",
        *,
        constants_only: bool = False
    ) -> "SnapshotDiffTuple":
        """
        Compares two snapshots and returns the diff analysis result.
        Allows filtering to include only constant (atomic) elements.
        """
        ...