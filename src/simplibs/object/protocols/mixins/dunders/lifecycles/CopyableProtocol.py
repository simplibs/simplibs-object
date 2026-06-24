from typing import Protocol, runtime_checkable, Any, Self
# Outers
from ...core_mixins import NodesDictsProtocol, SnapshotProtocol


@runtime_checkable
class CopyableProtocol(
    NodesDictsProtocol,
    SnapshotProtocol,
    Protocol
):
    """
    Protokol pro mixin Copyable.

    Garantuje podporu pro standardní mělké a hluboké kopírování objektu 
    v rámci Python ekosystému (integrace s modulem copy). Strategie se 
    uvnitř přizpůsobuje stavu mutability, navenek ale vždy vrací identický typ (Self).
    """

    def __copy__(self) -> Self:
        """
        Vytvoří a vrátí mělkou kopii (shallow copy) této instance.
        Bezpečně reaguje na mutable/immutable režim objektu.
        """
        ...

    def __deepcopy__(self, memo: dict[int, Any]) -> Self:
        """
        Vytvoří a vrátí hlubokou kopii (deep copy) této instance.
        Slovník `memo` slouží k internímu sledování již navštívených 
        objektů kvůli zamezení zacyklení.
        """
        ...