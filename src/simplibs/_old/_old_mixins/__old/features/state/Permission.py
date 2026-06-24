from typing import TYPE_CHECKING
# Outers
from ...base_class import SimpleMixin
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

    __slots__ = ("_locked",)

    # ---------------------------------------------------------
    # Inicializace mixinu
    # ---------------------------------------------------------

    def init_mixins(self):
        super().init_mixins()
        object.__setattr__(self, "_locked", False)

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

    # ---------------------------------------------------------
    # Hooks
    # ---------------------------------------------------------

    def _before_update(self, new_value):
        """Hook který se volá před uložením hodnoty"""
        if self._locked:
            raise ValueError(f"{self.__class__.__name__} is locked.")
        # noinspection PyUnresolvedReferences
        super()._before_update(new_value)

