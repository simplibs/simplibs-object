from typing import Protocol, runtime_checkable, Self, TYPE_CHECKING
# Outers
from ..core_mixins.SnapshotProtocol import SnapshotProtocol
# Annotations
if TYPE_CHECKING:
    from ...alias_typings import SnapshotTuple


@runtime_checkable
class DefaultStateProtocol(
    SnapshotProtocol,
    Protocol
):
    """
    Protocol for the DefaultState mixin.

    Guarantees the instance's ability to maintain its default state, reset to it,
    create fresh new default instances, or clone its current state.
    """

    # --- TECHNICAL ATTRIBUTES (Initialized in init_mixins) ---

    # Stores a state snapshot of values taken at the moment of instance creation
    _default_state_snapshot: "SnapshotTuple"

    # --- PUBLIC STATE MANAGEMENT API ---

    def clone_instance(self) -> Self:
        """Creates and returns a new instance with the same current state as this instance."""
        ...

    def reset_to_default_values(self) -> None:
        """Resets the internal state of the entire instance to its initial creation state."""
        ...

    def create_new_default_instance(self) -> Self:
        """
        Creates and returns a completely new, clean instance of the same type
        with default values defined in the blueprint.
        """
        ...