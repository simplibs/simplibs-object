from typing import TYPE_CHECKING
# Outers
from ..core_mixins import Snapshot
from .._commons.immutability import create_new_instance
# Annotations
if TYPE_CHECKING:
    from ..._core.protocols.mixins.state import DefaultStateProtocol
    from ..._core.protocols.alias_typings import SnapshotTuple



# noinspection PyProtectedMember
class DefaultState(Snapshot):
    """
    Mixin, který instanci poskytne:
    - uložený výchozí stav (_default_state)
    - metody clone_instance(), reset_to_default_values(), create_new_default_instance()
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice určení
    _mutable_only = True

    # Definice slotů
    __slots__ = ("_default_state_snapshot",)

    # ----------------------------------------
    # Hook pro inicializaci
    # ----------------------------------------

    # noinspection PyAttributeOutsideInit
    def init_mixins(
        self: "DefaultStateProtocol"
    ) -> None:
        """
        Metoda, předávající svojí logiku do inicializačního procesu instance.
        """

        # 1. Inicializace předků
        super().init_mixins()

        # 2. Vytvoření snapshotu defaultního stavu
        self._default_state_snapshot: "SnapshotTuple" = self._build_snapshot()

    # ----------------------------------------
    # Metods - CLONE / RESET / NEW
    # ----------------------------------------

    def clone_instance(
        self: "DefaultStateProtocol"
    ) -> "DefaultStateProtocol":
        """Vytvoří novou instanci se stejným stavem jako tato instance."""
        new_instance = self.create_new_default_instance()
        new_instance._restore_snapshot(self._build_snapshot())
        return new_instance

    def reset_to_default_values(
        self: "DefaultStateProtocol"
    ) -> None:
        """Resetuje instanci do výchozího stavu (_default_state)."""
        self._restore_snapshot(self._default_state_snapshot)

    # noinspection PyTypeChecker
    def create_new_default_instance(
        self: "DefaultStateProtocol"
    ) -> "DefaultStateProtocol":
        """
        Vrátí novou instanci stejného typu se stejným výchozím stavem,
        jaký měla tato instance při svém vzniku.
        """
        return create_new_instance(self, self._default_state_snapshot)


