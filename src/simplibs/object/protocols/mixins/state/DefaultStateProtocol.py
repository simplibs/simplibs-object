from typing import Protocol, runtime_checkable, Self, Any
# Outers
from ..core_mixins.SnapshotProtocol import SnapshotProtocol


@runtime_checkable
class DefaultStateProtocol(
    SnapshotProtocol,
    Protocol
):
    """
    Protokol pro mixin DefaultState.

    Garantuje schopnost instance uchovávat svůj výchozí stav, resetovat se do něj,
    vytvářet čisté nové defaultní instance nebo klonovat svůj aktuální stav.
    """

    # --- TECHNICKÉ ATRIBUTY (Inicializované v init_mixins) ---

    # Uchovává otisk stavu (snapshot) hodnot v momentu vzniku instance
    _default_state_snapshot: tuple[Any, ...]

    # --- VEŘEJNÉ API PRO SPRÁVU STAVU ---

    def clone_instance(self) -> Self:
        """Vytvoří a vrátí novou instanci se stejným aktuálním stavem jako tato instance."""
        ...

    def reset_to_default_values(self) -> None:
        """Resetuje vnitřní stav celé instance do její výchozí podoby při vzniku."""
        ...

    def create_new_default_instance(self) -> Self:
        """
        Vytvoří a vrátí zcela novou, čistou instanci stejného typu
        s výchozími hodnotami definovanými v blueprintu.
        """
        ...