from typing import TYPE_CHECKING
# Outers
from ..base_class import SimpleMixin
# Annotations
if TYPE_CHECKING:
    from ....protocols import SimpleInstanceType


# noinspection PyProtectedMember
class Permission(SimpleMixin):
    """
    Read-only režim — zamykání proti změnám.

    Příklad:
        obj.lock()
        obj.value = 10  # → ValueError
    """

    # Definice určení
    _mutable_only = True

    # Definice slotů
    __slots__ = ()

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def is_locked(self) -> bool:
        """Vrací bool zda je zámek aktivní"""
        return self._locked

    # ---------------------------------------------------------
    # Methods
    # ---------------------------------------------------------

    def lock(self):
        """Zamyká zámek"""
        object.__setattr__(self, "_locked", True)

    def unlock(self):
        """Odemyká zámek"""
        object.__setattr__(self, "_locked", False)

