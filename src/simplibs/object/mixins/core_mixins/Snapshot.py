# Inners
from .NodesTuple import NodesTuple
from ._utils.snapshot import compare_snapshots


# noinspection PyProtectedMember
class Snapshot(NodesTuple):
    """
    Ukládá kompletní snapshoty stavu instance a umožňuje jejich obnovu.
    Snapshot je čisté tuple hodnot ve stejném pořadí jako _nodes_tuple.
    """

    __slots__ = ()


    def _build_snapshot(self) -> tuple:
        """Vytvoří snapshot jako tuple hodnot dle _nodes_tuple."""
        return tuple(instance._value for instance, _ in self._nodes_tuple)

    def _restore_snapshot(self, snapshot: tuple) -> None:
        """Obnoví stav instance ze snapshotu."""
        for (instance, _), value in zip(self._nodes_tuple, snapshot):
            instance._value = value

    def _compare_snapshots(self,
        snapshot1: tuple,
        snapshot2: tuple,
        *,
        constants_only: bool = False
    ) -> tuple:
        """ Porovná dva snapshoty"""
        return compare_snapshots(
            self._nodes_tuple,
            snapshot1,
            snapshot2,
            constants_only=constants_only
        )


