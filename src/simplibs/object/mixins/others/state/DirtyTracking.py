from typing import TYPE_CHECKING
# Outers
from ...core_mixins import Snapshot
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.state import DirtyTrackingProtocol
    from ...._core.protocols.alias_typings import SnapshotDiffTuple, SnapshotTuple


class DirtyTracking(Snapshot):
    """
    Modern snapshot-based dirty tracking.
    Works for atoms, composites, and nested structures.
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Compatibility declaration
    _mutable_only = True

    # Slot definition
    __slots__ = ("_clean_snapshot",)

    # ----------------------------------------
    # Initialization hook
    # ----------------------------------------

    # noinspection PyAttributeOutsideInit
    def init_mixins(
        self: "DirtyTrackingProtocol"
    ) -> None:
        """
        Method forwarding its logic into the instance's initialization
        process.
        """

        # 1. Build a snapshot of the default state
        self._clean_snapshot = self._build_snapshot()

    # ----------------------------------------
    # Property - getters
    # ----------------------------------------

    @property
    def is_dirty(
        self: "DirtyTrackingProtocol"
    ) -> bool:
        """True if the current state differs from the clean snapshot."""
        current_snapshot = self._build_snapshot()
        return current_snapshot != self._clean_snapshot

    @property
    def dirty_paths(
        self: "DirtyTrackingProtocol"
    ) -> "SnapshotDiffTuple":
        """Returns a tuple of changed paths (path, old_value, new_value)."""
        current_snapshot = self._build_snapshot()
        return self._compare_snapshots(
            self._clean_snapshot,
            current_snapshot,
            constants_only=True
        )

    @property
    def clean_snapshot(
        self: "DirtyTrackingProtocol"
    ) -> "SnapshotTuple":
        return self._clean_snapshot

    # ----------------------------------------
    # Methods - GET DIRTY / RESET / MARK CLEAN
    # ----------------------------------------

    def get_dirty_paths(
        self: "DirtyTrackingProtocol",
        *,
        constants_only: bool = True
    ) -> "SnapshotDiffTuple":
        """Returns changed paths, with the option to include only constants or everything."""
        return self._compare_snapshots(
            self._clean_snapshot,
            self._build_snapshot(),
            constants_only=constants_only
        )

    def reset_to_clean(
        self: "DirtyTrackingProtocol"
    ) -> None:
        """Restores the object to its clean snapshot."""
        self._restore_snapshot(self._clean_snapshot)

    def mark_clean(
        self: "DirtyTrackingProtocol"
    ) -> None:
        """Marks the current state as the new clean snapshot."""
        # noinspection PyAttributeOutsideInit
        self._clean_snapshot = self._build_snapshot()


_DESIGN_NOTES = """
# DirtyTracking

## Purpose
Tracks whether a mutable instance has changed since a reference point —
`is_dirty`, `dirty_paths`, `reset_to_clean()`, `mark_clean()` — the same
concept as "unsaved changes" indicators in editors, but generalized to
any Simple instance, including nested composites.

## Compatibility
- `_mutable_only = True` — "dirty" only means something relative to
  in-place changes; an immutable instance never mutates, so it can never
  become dirty in this sense.

## Logic
- On `init_mixins`, a `_clean_snapshot` is captured immediately — the
  instance starts out "clean" by definition, relative to its own initial
  state.
- `is_dirty` rebuilds a fresh snapshot and compares it against
  `_clean_snapshot` for inequality — a full snapshot comparison on every
  access, not a cached flag that's incrementally updated on each write.
- `dirty_paths` and `get_dirty_paths(constants_only=...)` both delegate
  to `_compare_snapshots` (from `Snapshot`), turning positional
  differences into meaningful `(path, old, new)` triples.
  `dirty_paths` is a fixed `constants_only=True` property; `get_dirty_paths`
  is the more flexible method form, letting a caller include
  composite-level changes too.
- `reset_to_clean()` restores the instance back to `_clean_snapshot`,
  discarding all changes since the last clean mark.
- `mark_clean()` re-captures the current state as the new baseline —
  useful after a "save" operation, where the current dirty state should
  become the new clean reference point.

## Notes
- "Modern" in the class docstring implies a prior, presumably
  attribute-flag-based dirty-tracking approach existed before this
  snapshot-based one — worth knowing if older code or docs reference a
  different mechanism.
- Every dirty check does a full snapshot rebuild and comparison rather
  than tracking writes incrementally — simple and correct, but worth
  keeping in mind for very large composites where this could become a
  noticeable cost if checked frequently.
"""
