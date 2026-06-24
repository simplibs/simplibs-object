import operator
from numbers import Number
# Outers
from ...core_mixins import NodesDicts, Snapshot
# Inners
from ._utils.arithmetic import execute_op, execute_rop



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

    __slots__ = ()

    # Omezení na číselné typy
    _only_types = Number

    # -------------------------
    # Sčítání (+)
    # -------------------------
    def __add__(self, other):
        """Vrací novou instanci s hodnotou self.value + other (s lazy fallback konverzí)."""
        return execute_op(self, operator.add, other)

    def __radd__(self, other):
        """Vrací novou instanci s hodnotou other + self.value (s lazy fallback konverzí)."""
        return execute_rop(self, operator.add, other)

    # -------------------------
    # Odčítání (-)
    # -------------------------
    def __sub__(self, other):
        """Vrací novou instanci s hodnotou self.value - other (s lazy fallback konverzí)."""
        return execute_op(self, operator.sub, other)

    def __rsub__(self, other):
        """Vrací novou instanci s hodnotou other - self.value (s lazy fallback konverzí)."""
        return execute_rop(self, operator.sub, other)

    # -------------------------
    # Násobení (*)
    # -------------------------
    def __mul__(self, other):
        """Vrací novou instanci s hodnotou self.value * other (s lazy fallback konverzí)."""
        return execute_op(self, operator.mul, other)

    def __rmul__(self, other):
        """Vrací novou instanci s hodnotou other * self.value (s lazy fallback konverzí)."""
        return execute_rop(self, operator.mul, other)

    # -------------------------
    # Dělení (/)
    # -------------------------
    def __truediv__(self, other):
        """Vrací novou instanci s hodnotou self.value / other (s lazy fallback konverzí)."""
        return execute_op(self, operator.truediv, other)

    def __rtruediv__(self, other):
        """Vrací novou instanci s hodnotou other / self.value (s lazy fallback konverzí)."""
        return execute_rop(self, operator.truediv, other)

    # -------------------------
    # Celočíselné dělení (//)
    # -------------------------
    def __floordiv__(self, other):
        """Vrací novou instanci s hodnotou self.value // other (s lazy fallback konverzí)."""
        return execute_op(self, operator.floordiv, other)

    def __rfloordiv__(self, other):
        """Vrací novou instanci s hodnotou other // self.value (s lazy fallback konverzí)."""
        return execute_rop(self, operator.floordiv, other)

    # -------------------------
    # Modulo (%)
    # -------------------------
    def __mod__(self, other):
        """Vrací novou instanci s hodnotou self.value % other (s lazy fallback konverzí)."""
        return execute_op(self, operator.mod, other)

    def __rmod__(self, other):
        """Vrací novou instanci s hodnotou other % self.value (s lazy fallback konverzí)."""
        return execute_rop(self, operator.mod, other)

    # -------------------------
    # Mocnina (**)
    # -------------------------
    def __pow__(self, other):
        """Vrací novou instanci s hodnotou self.value ** other (s lazy fallback konverzí)."""
        return execute_op(self, operator.pow, other)

    def __rpow__(self, other):
        """Vrací novou instanci s hodnotou other ** self.value (s lazy fallback konverzí)."""
        return execute_rop(self, operator.pow, other)