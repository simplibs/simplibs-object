from typing import TYPE_CHECKING, Any
from datetime import datetime
# Outers
from ..core_mixins import Serialization
# Inners
from ._history_utils.core import set_history_limit, record_state, find_snapshot
from ._history_utils.transfer import export_history_to_dict, import_history_from_dict
from ._history_utils.navigations import (
    history_undo,
    history_redo,
    go_to_last_history,
    go_to_history_on_timestamp,
    go_to_history_on_index
)
# Annotations
if TYPE_CHECKING:
    from ..._core.protocols.mixins.state import HistoryProtocol
    from ..._core.protocols.alias_typings import HistoryEntry, HistoryDict, SnapshotDiffTuple


class History(Serialization):
    """
    Provides a full undo/redo history for a mutable instance.

    Every state-changing action can be recorded as a timestamped snapshot.
    The history can be navigated step by step (undo/redo), jumped to by
    index or timestamp, diffed between any two recorded points, and
    exported to / imported from a dict for persistence.
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Compatibility declaration
    _mutable_only = True

    # Slot definition
    __slots__ = (
        "_history",
        "_history_index",
        "_history_limit",
        "_history_count"
    )

    # ----------------------------------------
    # Initialization hook
    # ----------------------------------------

    # noinspection PyAttributeOutsideInit
    def init_mixins(
        self: "HistoryProtocol"
    ) -> None:
        """
        Method forwarding its logic into the instance's initialization
        process.
        """

        # 1. Initialize parents
        super().init_mixins()

        # 2. Create internal elements
        self._history: list["HistoryEntry"] = []
        self._history_limit: int | None  = None
        self._history_index: int = 0
        self._history_count: int = 0

        # 3. Create the first entry
        self.record_state()

    # ----------------------------------------
    # Initialization-related method
    # ----------------------------------------

    def record_state(
        self: "HistoryProtocol"
    ) -> "HistoryEntry":
        """Creates a snapshot of the current state and saves it to history."""
        return record_state(self)

    # ----------------------------------------
    # Property - getters
    # ----------------------------------------

    @property
    def history(
        self: "HistoryProtocol"
    ) -> tuple["HistoryEntry", ...]:
        """Returns the history as a tuple."""
        return tuple(self._history)

    @property
    def history_index(
        self: "HistoryProtocol"
    ) -> int | None:
        """Returns the index of the latest history entry."""
        return self._history_index

    @property
    def history_limit(
        self: "HistoryProtocol"
    ) -> int | None:
        """Returns the history size limit."""
        return self._history_limit

    # ----------------------------------------
    # Property - setters
    # ----------------------------------------

    @history_limit.setter
    def history_limit(
        self: "HistoryProtocol",
        value: int
    ) -> None:
        """Sets the history size limit."""
        set_history_limit(self, value)

    # ----------------------------------------
    # Methods - UNDO / REDO
    # ----------------------------------------

    def undo(
        self: "HistoryProtocol"
    ) -> bool:
        """Method for moving to the previous entry (if it exists)."""
        return history_undo(self)

    def redo(
        self: "HistoryProtocol"
    ) -> bool:
        """Method for moving to the next entry (if it exists)."""
        return history_redo(self)

    # ----------------------------------------
    # Methods - GOTO
    # ----------------------------------------

    def go_to_last(
        self: "HistoryProtocol"
    ) -> None:
        """Method for moving to the last history entry."""
        go_to_last_history(self)

    def go_to_index(
        self: "HistoryProtocol",
        index: int
    ) -> None:
        """Method for moving to a specific index."""
        go_to_history_on_index(self, index)

    def go_to_timestamp(
        self: "HistoryProtocol",
        timestamp: datetime
    ) -> None:
        """Method for moving to a specific timestamp."""
        go_to_history_on_timestamp(self, timestamp)

    # ----------------------------------------
    # Methods - EXPORT / IMPORT
    # ----------------------------------------

    def export_history_to_dict(
        self: "HistoryProtocol"
    ) -> "HistoryDict":
        """Exports the history to a dict."""
        return export_history_to_dict(self)

    def import_history_from_dict(
        self: "HistoryProtocol",
        history_dict: "HistoryDict"
    ) -> None:
        """Imports the history from a dict."""
        import_history_from_dict(self, history_dict)

    # ----------------------------------------
    # Methods - REMOVE / DIFF
    # ----------------------------------------

    def remove_history_limit(
        self: "HistoryProtocol"
    ) -> None:
        """Removes the history size limit."""
        # noinspection PyAttributeOutsideInit
        self._history_limit = None

    def diff(
        self: "HistoryProtocol",
        snap1: int | datetime,
        snap2: int | datetime,
        *,
        constants_only: bool = False
    ) -> "SnapshotDiffTuple":
        """Compares two snapshots — returns a tuple of changed (path, old_value, new_value)."""
        return self._compare_snapshots(
            find_snapshot(self, snap1),
            find_snapshot(self, snap2),
            constants_only=constants_only
        )


_DESIGN_NOTES = """
# History

## Purpose
Full undo/redo history for a mutable instance — records snapshots over
time, lets you step backward/forward, jump to a specific index or
timestamp, diff any two recorded states, and export/import the whole
history as a dict.

## Compatibility
- `_mutable_only = True` — history tracks in-place mutations over time;
  an immutable instance has no in-place timeline to record.

## Logic
`History` is mostly a thin coordinating layer over the
`_history_utils` package, which does the heavy lifting:

- **Recording**: `init_mixins` sets up empty `_history`/`_history_index`/
  `_history_limit`/`_history_count`, then immediately calls
  `record_state()` once, so a freshly created instance already has one
  entry — its own starting state — rather than an empty history.
  `record_state()` itself delegates to the `record_state` utility.
- **Limit management**: `history_limit` is a property with both a
  getter (plain attribute read) and a setter that delegates to
  `set_history_limit` (presumably handling trimming older entries when
  the limit shrinks). `remove_history_limit()` bypasses that utility and
  sets `_history_limit = None` directly, since removing a limit needs no
  trimming logic.
- **Navigation**: `undo()`/`redo()` delegate to `history_undo`/
  `history_redo` and return a `bool` (presumably whether the move
  succeeded, e.g. `False` at the start/end of history). `go_to_last()`,
  `go_to_index()`, `go_to_timestamp()` delegate to their matching
  `_history_utils.navigations` functions.
- **Export/import**: `export_history_to_dict()`/
  `import_history_from_dict()` delegate straight to the `transfer`
  utilities — this is what makes history itself serializable, separate
  from the instance's own `to_dict()`/`from_dict()` in `Serialization`.
- **Diffing**: `diff(snap1, snap2, constants_only=...)` accepts either an
  index or a `datetime` for each side, resolves each via
  `find_snapshot`, then reuses `_compare_snapshots` (inherited via
  `Serialization` → `Infrastructure` → `Snapshot`) to produce the actual
  diff.

## Notes
- Builds on `Serialization` (not directly on `Snapshot`), since history
  export/import needs the same dict/JSON foundation the instance's own
  state serialization uses.
- `diff()`'s dual `int | datetime` snapshot selectors mean a caller never
  has to manually look up an entry first — `find_snapshot` handles both
  identification schemes.
"""
