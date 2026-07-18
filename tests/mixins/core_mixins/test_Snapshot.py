from typing import TYPE_CHECKING
# Inners
from .NodesTuple import NodesTuple
from ._utils.snapshot import compare_snapshots
# Annotations
if TYPE_CHECKING:
    from ...protocols.mixins.core_mixins import SnapshotProtocol
    from ...protocols.alias_typings import SnapshotTuple, SnapshotDiffTuple


class Snapshot(NodesTuple):
    """
    Ukládá kompletní snapshoty stavu instance a umožňuje jejich obnovu.
    Snapshot je čisté tuple hodnot ve stejném pořadí jako _nodes_tuple.
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice slotů
    __slots__ = ()

    # ----------------------------------------
    # Methods - BUILD / RESTORE / COMPARE
    # ----------------------------------------

    def _build_snapshot(
        self: "SnapshotProtocol"
    ) -> "SnapshotTuple":
        """Vytvoří snapshot jako tuple hodnot dle _nodes_tuple."""
        # noinspection PyProtectedMember
        return tuple(
            instance._value for instance, _
            in self._nodes_tuple
        )

    def _restore_snapshot(
        self: "SnapshotProtocol",
        snapshot: "SnapshotTuple"
    ) -> None:
        """Obnoví stav instance ze snapshotu."""
        for (instance, _), value in zip(self._nodes_tuple, snapshot):
            instance._value = value

    def _compare_snapshots(
        self: "SnapshotProtocol",
        snapshot1: "SnapshotTuple",
        snapshot2: "SnapshotTuple",
        *,
        constants_only: bool = False
    ) -> "SnapshotDiffTuple":
        """ Porovná dva snapshoty"""
        return compare_snapshots(
            self._nodes_tuple,
            snapshot1,
            snapshot2,
            constants_only=constants_only
        )


