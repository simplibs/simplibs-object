from typing import Protocol, runtime_checkable, Any, Self
# Outers
from ...core_mixins import NodesDictsProtocol, SnapshotProtocol


@runtime_checkable
class ArithmeticProtocol(
    NodesDictsProtocol,
    SnapshotProtocol,
    Protocol
):
    """
    Protokol pro mixin Arithmetic.

    Garantuje kompletní sadu standardních i pravostranných aritmetických
    operátorů (+, -, *, /, //, %, **) s integrovanou bezpečnou konverzí typů.
    Všechny operace jsou čisté a vracejí novou instanci stejného typu (Self).
    """

    # ---------------------------------------------------------
    # Sčítání (+)
    # ---------------------------------------------------------
    def __add__(self, other: Any) -> Self:
        """Vrací novou instanci s hodnotou (self.value + other)."""
        ...

    def __radd__(self, other: Any) -> Self:
        """Pravostranné sčítání. Vrací novou instanci s hodnotou (other + self.value)."""
        ...

    # ---------------------------------------------------------
    # Odčítání (-)
    # ---------------------------------------------------------
    def __sub__(self, other: Any) -> Self:
        """Vrací novou instanci s hodnotou (self.value - other)."""
        ...

    def __rsub__(self, other: Any) -> Self:
        """Pravostranné odčítání. Vrací novou instanci s hodnotou (other - self.value)."""
        ...

    # ---------------------------------------------------------
    # Násobení (*)
    # ---------------------------------------------------------
    def __mul__(self, other: Any) -> Self:
        """Vrací novou instanci s hodnotou (self.value * other)."""
        ...

    def __rmul__(self, other: Any) -> Self:
        """Pravostranné násobení. Vrací novou instanci s hodnotou (other * self.value)."""
        ...

    # ---------------------------------------------------------
    # Dělení (/)
    # ---------------------------------------------------------
    def __truediv__(self, other: Any) -> Self:
        """Vrací novou instanci s hodnotou (self.value / other)."""
        ...

    def __rtruediv__(self, other: Any) -> Self:
        """Pravostranné dělení. Vrací novou instanci s hodnotou (other / self.value)."""
        ...

    # ---------------------------------------------------------
    # Celočíselné dělení (//)
    # ---------------------------------------------------------
    def __floordiv__(self, other: Any) -> Self:
        """Vrací novou instanci s hodnotou (self.value // other)."""
        ...

    def __rfloordiv__(self, other: Any) -> Self:
        """Pravostranné celočíselné dělení. Vrací novou instanci s hodnotou (other // self.value)."""
        ...

    # ---------------------------------------------------------
    # Modulo (%)
    # ---------------------------------------------------------
    def __mod__(self, other: Any) -> Self:
        """Vrací novou instanci s hodnotou (self.value % other)."""
        ...

    def __rmod__(self, other: Any) -> Self:
        """Pravostranné modulo. Vrací novou instanci s hodnotou (other % self.value)."""
        ...

    # ---------------------------------------------------------
    # Mocnina (**)
    # ---------------------------------------------------------
    def __pow__(self, other: Any) -> Self:
        """Vrací novou instanci s hodnotou (self.value ** other)."""
        ...

    def __rpow__(self, other: Any) -> Self:
        """Pravostranné umocňování. Vrací novou instanci s hodnotou (other ** self.value)."""
        ...