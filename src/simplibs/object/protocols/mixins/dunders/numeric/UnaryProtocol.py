from typing import Protocol, runtime_checkable, Self
# Outers
from ...core_mixins import NodesDictsProtocol, SnapshotProtocol


@runtime_checkable
class UnaryProtocol(
    NodesDictsProtocol,
    SnapshotProtocol,
    Protocol
):
    """
    Protokol pro mixin Unary.

    Garantuje sadu unárních numerických operátorů (-x, +x, abs(x)).
    Všechny operace jsou čisté a vracejí novou instanci téhož typu (Self).
    """

    # ---------------------------------------------------------
    # Unární operace znamének
    # ---------------------------------------------------------
    def __neg__(self) -> Self:
        """Matematická negace. Vrací novou instanci s hodnotou (-self.value)."""
        ...

    def __pos__(self) -> Self:
        """Unární plus. Vrací novou instanci s hodnotou (+self.value)."""
        ...

    # ---------------------------------------------------------
    # Absolutní hodnota
    # ---------------------------------------------------------
    def __abs__(self) -> Self:
        """Vrací novou instanci s absolutní hodnotou: abs(self.value)."""
        ...