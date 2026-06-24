import operator
from numbers import Number
# Outers
from ...core_mixins import NodesDicts, Snapshot
# Inners
from ._utils.unary import execute_unary_op


class Unary(NodesDicts, Snapshot):
    """
    Poskytuje unární numerické operace (-x, +x, abs(x)) pro SimpleObject.

    Podporuje:
    - atomy (konstanty)
    - kompozice (přepočítává vnitřní inners i vlastnické owner hodnoty)

    Obsahuje lazy fallback konverzi typu:
    - pokud operace selže, pokusí se převést hodnotu na typ defaultní hodnoty
    - konverze se provádí pouze pokud je bezpečná (např. int → float/Decimal/Fraction)
    """

    __slots__ = ()

    # Omezení na číselné typy
    _only_types = Number

    # ---------------------------------------------------------
    # Unární operátory (-x, +x, abs(x))
    # ---------------------------------------------------------
    def __neg__(self):
        """Vrací novou instanci s hodnotou -self.value."""
        return execute_unary_op(self, operator.neg)

    def __pos__(self):
        """Vrací novou instanci s hodnotou +self.value."""
        return execute_unary_op(self, operator.pos)

    def __abs__(self):
        """Vrací novou instanci s hodnotou abs(self.value)."""
        return execute_unary_op(self, abs)