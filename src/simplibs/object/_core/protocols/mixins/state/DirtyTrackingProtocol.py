from typing import Protocol, runtime_checkable, TYPE_CHECKING
# Outers
from ..core_mixins.SnapshotProtocol import SnapshotProtocol
# Annotations
if TYPE_CHECKING:
    from ...alias_typings import SnapshotTuple, SnapshotDiffTuple


@runtime_checkable
class DirtyTrackingProtocol(
    SnapshotProtocol,
    Protocol
):
    """
    Protocol for the DirtyTracking mixin.

    Guarantees the ability to track state changes (dirty tracking) across the object hierarchy
    against a stored "clean" snapshot, retrieve modified paths, and reset state.
    """

    # --- TECHNICAL ATTRIBUTES (Initialized in init_mixins) ---

    # Stores a state snapshot considered as the default "clean" (unmodified) baseline
    _clean_snapshot: "SnapshotTuple"

    # --- ERGONOMIC PROPERTIES ---

    @property
    def is_dirty(self) -> bool:
        """Returns True if the current hierarchy state differs from the clean snapshot."""
        ...

    @property
    def dirty_paths(self) -> "SnapshotDiffTuple":
        """
        Returns a tuple of modified atomic element paths.
        Each element in the tuple consists of a triplet: (element_path, old_value, new_value).
        """
        ...

    @property
    def clean_snapshot(self) -> "SnapshotTuple":
        """Access to the currently stored clean snapshot."""
        ...

    # --- PUBLIC CHANGE TRACKING API ---

    def get_dirty_paths(self, *, constants_only: bool = True) -> "SnapshotDiffTuple":
        """
        Returns a tuple of detected hierarchy changes.
        Allows selecting whether to track only constants (atoms) or composite nodes as well.
        """
        ...

    def reset_to_clean(self) -> None:
        """Restores the complete internal state of all elements from the clean snapshot (discards changes)."""
        ...

    def mark_clean(self) -> None:
        """Marks the current state of the entire instance as the new baseline 'clean' state."""
        ...