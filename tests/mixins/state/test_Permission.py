from typing import TYPE_CHECKING
# Outers
from ..base_class import SimpleMixin
# Annotations
if TYPE_CHECKING:
    from ...protocols.mixins.state import PermissionProtocol


class Permission(SimpleMixin):
    """
    Read-only režim — zamykání proti změnám.

    Příklad:
        obj.lock()
        obj.value = 10  # → ValueError
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice určení
    _mutable_only = True

    # Definice slotů
    __slots__ = ()

    # ----------------------------------------
    # Property - getters
    # ----------------------------------------

    @property
    def is_locked(
        self: "PermissionProtocol"
    ) -> bool:
        """Vrací bool zda je zámek aktivní"""
        return self._locked

    # ----------------------------------------
    # Methods - LOCK / UNLOCK
    # ----------------------------------------

    def lock(
        self: "PermissionProtocol"
    ) -> None:
        """Zamyká zámek"""
        object.__setattr__(self, "_locked", True)

    def unlock(
        self: "PermissionProtocol"
    ) -> None:
        """Odemyká zámek"""
        object.__setattr__(self, "_locked", False)

