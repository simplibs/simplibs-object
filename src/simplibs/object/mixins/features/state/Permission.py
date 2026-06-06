# Outers
from ..base_class import SimpleMixin


class PermissionMixin(SimpleMixin):
    """
    Read-only režim — zamykání proti změnám.

    Příklad:
        obj.lock()
        obj.value = 10  # → ValueError
    """

    __slots__ = ("_locked",)

    def init_mixins(self):
        super().init_mixins()
        object.__setattr__(self, "_locked", False)

    @property
    def is_locked(self) -> bool:
        return self._locked

    def lock(self):
        object.__setattr__(self, "_locked", True)

    def unlock(self):
        object.__setattr__(self, "_locked", False)

    # HOOK: volá se PŘED změnou hodnoty
    def _before_update(self, new_value):
        if self._locked:
            raise ValueError(f"{self.__class__.__name__} is locked.")
        super()._before_update(new_value)

