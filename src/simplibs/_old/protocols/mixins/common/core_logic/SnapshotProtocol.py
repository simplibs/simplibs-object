from typing import Protocol, runtime_checkable, Any
# Inners
from .NodesTupleProtocol import NodesTupleProtocol


@runtime_checkable
class SnapshotProtocol(NodesTupleProtocol, Protocol):
    """
    Protokol pro mixin Snapshot.

    Definuje rozhraní pro vytváření, obnovu a porovnávání kompletních
    otisků stavu (snapshots) celé hierarchie prvků.
    """

    # Mixin nemá žádné vlastní sloty/atributy, definujeme pouze metody.

    def _build_snapshot(self) -> tuple[Any, ...]:
        """Vytvoří a vrátí snapshot jako čisté tuple hodnot všech sub-node prvků."""
        ...

    def _restore_snapshot(self, snapshot: tuple[Any, ...]) -> None:
        """Obnoví vnitřní stav všech sub-node prvků ze zadaného snapshotu."""
        ...

    def _compare_snapshots(
        self,
        snapshot1: tuple[Any, ...],
        snapshot2: tuple[Any, ...],
        *,
        constants_only: bool = False
    ) -> tuple[Any, ...]:
        """
        Porovná dva snapshoty a vrátí výsledek analýzy rozdílů.
        Umožňuje filtraci pouze na konstantní (atomické) prvky.
        """
        ...