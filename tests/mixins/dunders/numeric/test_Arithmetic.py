from typing import TYPE_CHECKING, Any
import operator
from numbers import Number
# Outers
from ...core_mixins import NodesDicts, Snapshot
# Inners
from ._utils import execute_arithmetic_op
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.dunders.numeric import ArithmeticProtocol


class Arithmetic(NodesDicts, Snapshot):
    """
    Poskytuje aritmetické operace (+, -, *, /, //, %, **) pro SimpleObject.

    Podporuje:
    - atomy (konstanty)
    - kompozice (přepočítává inners i owner hodnoty)

    Obsahuje lazy fallback konverzi typu:
    - pokud operace selže, pokusí se převést druhý operand na typ defaultní hodnoty
    - konverze se provádí pouze pokud je bezpečná (např. int → float/Decimal/Fraction)
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice určení
    _only_types = Number

    # Definice slotů
    __slots__ = ()

    # -------------------------
    # Methods - Sčítání (+)
    # -------------------------
    def __add__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Vrací novou instanci s hodnotou self.value + other (s lazy fallback konverzí)."""
        return execute_arithmetic_op(self, operator.add, other)

    def __radd__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Vrací novou instanci s hodnotou other + self.value (s lazy fallback konverzí)."""
        return execute_arithmetic_op(self, operator.add, other, is_reversed=True)

    # -------------------------
    # Methods - Odčítání (-)
    # -------------------------
    def __sub__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Vrací novou instanci s hodnotou self.value - other (s lazy fallback konverzí)."""
        return execute_arithmetic_op(self, operator.sub, other)

    def __rsub__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Vrací novou instanci s hodnotou other - self.value (s lazy fallback konverzí)."""
        return execute_arithmetic_op(self, operator.sub, other, is_reversed=True)

    # -------------------------
    # Methods - Násobení (*)
    # -------------------------
    def __mul__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Vrací novou instanci s hodnotou self.value * other (s lazy fallback konverzí)."""
        return execute_arithmetic_op(self, operator.mul, other)

    def __rmul__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Vrací novou instanci s hodnotou other * self.value (s lazy fallback konverzí)."""
        return execute_arithmetic_op(self, operator.mul, other, is_reversed=True)

    # -------------------------
    # Methods - Dělení (/)
    # -------------------------
    def __truediv__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Vrací novou instanci s hodnotou self.value / other (s lazy fallback konverzí)."""
        return execute_arithmetic_op(self, operator.truediv, other)

    def __rtruediv__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Vrací novou instanci s hodnotou other / self.value (s lazy fallback konverzí)."""
        return execute_arithmetic_op(self, operator.truediv, other, is_reversed=True)

    # -------------------------
    # Methods - Celočíselné dělení (//)
    # -------------------------
    def __floordiv__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Vrací novou instanci s hodnotou self.value // other (s lazy fallback konverzí)."""
        return execute_arithmetic_op(self, operator.floordiv, other)

    def __rfloordiv__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Vrací novou instanci s hodnotou other // self.value (s lazy fallback konverzí)."""
        return execute_arithmetic_op(self, operator.floordiv, other, is_reversed=True)

    # -------------------------
    # Methods - Modulo (%)
    # -------------------------
    def __mod__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Vrací novou instanci s hodnotou self.value % other (s lazy fallback konverzí)."""
        return execute_arithmetic_op(self, operator.mod, other)

    def __rmod__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Vrací novou instanci s hodnotou other % self.value (s lazy fallback konverzí)."""
        return execute_arithmetic_op(self, operator.mod, other, is_reversed=True)

    # -------------------------
    # Methods - Mocnina (**)
    # -------------------------
    def __pow__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Vrací novou instanci s hodnotou self.value ** other (s lazy fallback konverzí)."""
        return execute_arithmetic_op(self, operator.pow, other)

    def __rpow__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Vrací novou instanci s hodnotou other ** self.value (s lazy fallback konverzí)."""
        return execute_arithmetic_op(self, operator.pow, other, is_reversed=True)