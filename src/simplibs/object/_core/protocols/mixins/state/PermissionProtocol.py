from typing import Protocol, runtime_checkable
# Outers
from ..base_class import SimpleMixinProtocol


@runtime_checkable
class PermissionProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protocol for the Permission mixin.

    Works with the _lock attribute.

    Guarantees the ability to lock an instance against changes (Read-only mode)
    by activating an internal lock and validating via a pre-update hook.
    """

    # --- ERGONOMIC PROPERTIES ---

    @property
    def is_locked(self) -> bool:
        """Returns True if the instance is currently locked for writing."""
        ...

    # --- PUBLIC LOCK MANAGEMENT API ---

    def lock(self) -> None:
        """Locks the instance. Any attempt to modify the value will raise a ValueError."""
        ...

    def unlock(self) -> None:
        """Unlocks the instance, enabling value modification and updates once again."""
        ...