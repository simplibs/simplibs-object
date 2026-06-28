from typing import Protocol, runtime_checkable, TYPE_CHECKING
# Inners
from .NodesTupleProtocol import NodesTupleProtocol
# Annotations
if TYPE_CHECKING:
    from ...alias_typings import SnapshotTuple, SnapshotDiffTuple


@runtime_checkable
class SnapshotProtocol(
    NodesTupleProtocol,
    Protocol
):
    """
    Protokol pro mixin Snapshot.

    Definuje rozhraní pro vytváření, obnovu a porovnávání kompletních
    otisků stavu (snapshots) celé hierarchie prvků.
    """

    # Mixin nemá žádné vlastní sloty/atributy, definujeme pouze metody.

    def _build_snapshot(self) -> "SnapshotTuple":
        """Vytvoří a vrátí snapshot jako čisté tuple hodnot všech sub-node prvků."""
        ...

    def _restore_snapshot(self, snapshot: "SnapshotTuple") -> None:
        """Obnoví vnitřní stav všech sub-node prvků ze zadaného snapshotu."""
        ...

    def _compare_snapshots(
        self,
        snapshot1: "SnapshotTuple",
        snapshot2: "SnapshotTuple",
        *,
        constants_only: bool = False
    ) -> "SnapshotDiffTuple":
        """
        Porovná dva snapshoty a vrátí výsledek analýzy rozdílů.
        Umožňuje filtraci pouze na konstantní (atomické) prvky.
        """
        ...