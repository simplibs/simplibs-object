# Outers
from ..core_logic import Snapshot


# noinspection PyAttributeOutsideInit
# noinspection PyProtectedMember
class DefaultState(Snapshot):
    """
    Mixin, který instanci poskytne:
    - uložený výchozí stav (_default_state)
    - metody clone_instance(), reset_to_default_values(), create_new_default_instance()
    """

    __slots__ = ("_default_state_snapshot",)

    def init_mixins(self):
        super().init_mixins()
        self._default_state_snapshot = self._build_snapshot()

    # ---------------------------------------------------------
    # Klonování aktuální instance
    # ---------------------------------------------------------
    def clone_instance(self):
        """Vytvoří novou instanci se stejným stavem jako tato instance."""
        new_instance = self.create_new_default_instance()
        new_instance._restore_snapshot(self._build_snapshot())
        return new_instance

    # ---------------------------------------------------------
    # Reset hodnot do výchoz podoby
    # ---------------------------------------------------------
    def reset_to_default_values(self):
        """Resetuje instanci do výchozího stavu (_default_state)."""
        self._restore_snapshot(self._default_state_snapshot)

    # ---------------------------------------------------------
    # Vrátí novou instanci s defaultními hodnotami
    # ---------------------------------------------------------
    def create_new_default_instance(self):
        """Vrátí novou instanci, která odpovídá výchozímu stavu."""
        new_instance = object.__new__(type(self))
        new_instance.__init__()
        return new_instance


