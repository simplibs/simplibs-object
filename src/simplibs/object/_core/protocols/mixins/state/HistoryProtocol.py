from typing import Protocol, runtime_checkable, TYPE_CHECKING, Any
from datetime import datetime
# Outers
from ..core_mixins import SerializationProtocol
# Annotations
if TYPE_CHECKING:
    from ...alias_typings import HistoryEntry, HistoryDict, SnapshotDiffTuple


@runtime_checkable
class HistoryProtocol(
    SerializationProtocol,
    Protocol
):
    """
    Protocol for the History mixin.

    Guarantees complete timeline management for the object (Undo/Redo cascades),
    including navigation by index/timestamp, memory limit tracking,
    historical snapshot diff analysis, and full history export/import.
    """

    # --- TECHNICAL ATTRIBUTES (Initialized in init_mixins) ---
    _history: list["HistoryEntry"]    # Internal timeline records storage
    _history_limit: int | None       # Maximum allowed record capacity
    _history_index: int              # Pointer to the current timeline position
    _history_count: int              # Total count of actually stored records

    # --- INITIALIZATION AND RECORDING LOGIC ---

    def record_state(self) -> "HistoryEntry":
        """Creates a snapshot of the current state and appends it to the timeline."""
        ...

    # --- PROPERTIES ---

    @property
    def history(self) -> tuple["HistoryEntry", ...]:
        """Returns the full timeline history as an immutable tuple of records."""
        ...

    @property
    def history_index(self) -> int | None:
        """Returns the index of the current position (record) within the timeline."""
        ...

    @property
    def history_limit(self) -> int | None:
        """Returns the current history capacity limit, or None if unlimited."""
        ...

    @history_limit.setter
    def history_limit(self, value: int) -> None:
        """Sets the maximum history capacity limit."""
        ...

    # --- NAVIGATION API (Undo & Redo & GoTo) ---

    def undo(self) -> bool:
        """
        Moves the instance state one step back in time.
        Returns True if successful, False otherwise.
        """
        ...

    def redo(self) -> bool:
        """
        Moves the instance state one step forward in time.
        Returns True if successful, False otherwise.
        """
        ...

    def go_to_last(self) -> None:
        """Navigates the instance state to the latest (most recent) recorded entry."""
        ...

    def go_to_index(self, index: int) -> None:
        """Navigates the instance state to a record specified by a numerical index."""
        ...

    def go_to_timestamp(self, timestamp: datetime) -> None:
        """Navigates the instance state to a record corresponding to a specific timestamp."""
        ...

    # --- HISTORY EXPORT & IMPORT ---

    def export_history_to_dict(self) -> "HistoryDict":
        """Exports the complete timeline structure and data into a dictionary."""
        ...

    def import_history_from_dict(self, history_dict: "HistoryDict") -> None:
        """Imports and fully reconstructs the entire timeline from the provided dictionary."""
        ...

    def remove_history_limit(self) -> None:
        """Removes the history capacity limit entirely (unlimited timeline)."""
        ...

    # --- DIFF ANALYSIS ---

    def diff(
        self,
        snap1: int | datetime,
        snap2: int | datetime,
        *,
        constants_only: bool = False
    ) -> "SnapshotDiffTuple":
        """
        Compares two arbitrary history points (specified by index or timestamp).
        Returns a tuple of change triplets: (element_path, old_value, new_value).
        """
        ...