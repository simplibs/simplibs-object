import operator
from numbers import Number
# Outers
from ...base_class import SimpleMixin
#Inners
from ._utils.inplace import execute_inplace_op


class Inplace(SimpleMixin):
    """
    Poskytuje in‑place aritmetické operace (+=, -=, *=, /=, //=, %=, **=)
    pro SimpleObject atomy a mutable instance.

    Operace:
    - mění hodnotu instance přes self.value = ...
    - aktivují validaci a reaktivitu
    - vrací self
    """

    __slots__ = ()

    # Pouze pro číselné typy
    _only_types = Number

    # Pouze pro mutable objekty
    _mutable_only = True

    # ---------------------------------------------------------
    # Operátory (+=, -=, *=, /=, //=, %=, **=)
    # ---------------------------------------------------------
    def __iadd__(self, other):
        """In‑place: self.value += other."""
        return execute_inplace_op(self, operator.add, other)

    def __isub__(self, other):
        """In‑place: self.value -= other."""
        return execute_inplace_op(self, operator.sub, other)

    def __imul__(self, other):
        """In‑place: self.value *= other."""
        return execute_inplace_op(self, operator.mul, other)

    def __itruediv__(self, other):
        """In‑place: self.value /= other."""
        return execute_inplace_op(self, operator.truediv, other)

    def __ifloordiv__(self, other):
        """In‑place: self.value //= other."""
        return execute_inplace_op(self, operator.floordiv, other)

    def __imod__(self, other):
        """In‑place: self.value %= other."""
        return execute_inplace_op(self, operator.mod, other)

    def __ipow__(self, other):
        """In‑place: self.value **= other."""
        return execute_inplace_op(self, operator.pow, other)