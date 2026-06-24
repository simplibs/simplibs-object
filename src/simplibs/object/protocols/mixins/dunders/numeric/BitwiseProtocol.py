from typing import Protocol, runtime_checkable, Any, Self
# Outers
from ...core_mixins import NodesDictsProtocol, SnapshotProtocol


@runtime_checkable
class BitwiseProtocol(
    NodesDictsProtocol,
    SnapshotProtocol,
    Protocol
):
    """
    Protokol pro mixin Bitwise.

    Garantuje kompletní sadu bitových operátorů (&, |, ^, <<, >>, ~).
    Všechny operace jsou čisté a vracejí novou instanci stejného typu (Self).
    """

    # ---------------------------------------------------------
    # Operátor AND (&)
    # ---------------------------------------------------------
    def __and__(self, other: Any) -> Self:
        """Vrací novou instanci s hodnotou (self.value & other)."""
        ...

    def __rand__(self, other: Any) -> Self:
        """Pravostranný AND. Vrací novou instanci s hodnotou (other & self.value)."""
        ...

    # ---------------------------------------------------------
    # Operátor OR (|)
    # ---------------------------------------------------------
    def __or__(self, other: Any) -> Self:
        """Vrací novou instanci s hodnotou (self.value | other)."""
        ...

    def __ror__(self, other: Any) -> Self:
        """Pravostranný OR. Vrací novou instanci s hodnotou (other | self.value)."""
        ...

    # ---------------------------------------------------------
    # Operátor XOR (^)
    # ---------------------------------------------------------
    def __xor__(self, other: Any) -> Self:
        """Vrací novou instanci s hodnotou (self.value ^ other)."""
        ...

    def __rxor__(self, other: Any) -> Self:
        """Pravostranný XOR. Vrací novou instanci s hodnotou (other ^ self.value)."""
        ...

    # ---------------------------------------------------------
    # Operátor LSHIFT (<<)
    # ---------------------------------------------------------
    def __lshift__(self, other: Any) -> Self:
        """Bitový posun vlevo. Vrací novou instanci s hodnotou (self.value << other)."""
        ...

    def __rlshift__(self, other: Any) -> Self:
        """Pravostranný posun vlevo. Vrací novou instanci s hodnotou (other << self.value)."""
        ...

    # ---------------------------------------------------------
    # Operátor RSHIFT (>>)
    # ---------------------------------------------------------
    def __rshift__(self, other: Any) -> Self:
        """Bitový posun vpravo. Vrací novou instanci s hodnotou (self.value >> other)."""
        ...

    def __rrshift__(self, other: Any) -> Self:
        """Pravostranný posun vpravo. Vrací novou instanci s hodnotou (other >> self.value)."""
        ...

    # ---------------------------------------------------------
    # Operátor INVERT (~)
    # ---------------------------------------------------------
    def __invert__(self) -> Self:
        """Unární bitová inverze. Vrací novou instanci s hodnotou (~self.value)."""
        ...