import operator
from numbers import Integral
# Outers
from ...core_mixins import NodesDicts, Snapshot
from ..._shared_logic.immutability import with_constant
# Inners
from ._utils.bitwise import execute_bit_op, execute_bit_rop


class Bitwise(NodesDicts, Snapshot):
    """
    Poskytuje bitové operace (&, |, ^, <<, >>, ~) pro SimpleObject atomy.

    Vlastnosti:
    - funguje pouze pro atomy (konstanty)
    - funguje pouze pro integrální typy (int, vlastní integer-like typy)
    - operace jsou čisté → vrací novou instanci přes with_constant pipeline
    """

    __slots__ = ()

    # Pouze pro integrální typy
    _only_types = Integral

    # Pouze pro konstanty (atomy)
    _constant_only = True

    # ---------------------------------------------------------
    # & (Bitwise AND)
    # ---------------------------------------------------------
    def __and__(self, other):
        """Vrací novou instanci s hodnotou self.value & other."""
        return execute_bit_op(self, operator.and_, other)

    def __rand__(self, other):
        """Vrací novou instanci s hodnotou other & self.value."""
        return execute_bit_rop(self, operator.and_, other)

    # ---------------------------------------------------------
    # | (Bitwise OR)
    # ---------------------------------------------------------
    def __or__(self, other):
        """Vrací novou instanci s hodnotou self.value | other."""
        return execute_bit_op(self, operator.or_, other)

    def __ror__(self, other):
        """Vrací novou instanci s hodnotou other | self.value."""
        return execute_bit_rop(self, operator.or_, other)

    # ---------------------------------------------------------
    # ^ (Bitwise XOR)
    # ---------------------------------------------------------
    def __xor__(self, other):
        """Vrací novou instanci s hodnotou self.value ^ other."""
        return execute_bit_op(self, operator.xor, other)

    def __rxor__(self, other):
        """Vrací novou instanci s hodnotou other ^ self.value."""
        return execute_bit_rop(self, operator.xor, other)

    # ---------------------------------------------------------
    # << (Bitwise Left Shift)
    # ---------------------------------------------------------
    def __lshift__(self, other):
        """Vrací novou instanci s hodnotou self.value << other."""
        return execute_bit_op(self, operator.lshift, other)

    def __rlshift__(self, other):
        """Vrací novou instanci s hodnotou other << self.value."""
        return execute_bit_rop(self, operator.lshift, other)

    # ---------------------------------------------------------
    # >> (Bitwise Right Shift)
    # ---------------------------------------------------------
    def __rshift__(self, other):
        """Vrací novou instanci s hodnotou self.value >> other."""
        return execute_bit_op(self, operator.rshift, other)

    def __rrshift__(self, other):
        """Vrací novou instanci s hodnotou other >> self.value."""
        return execute_bit_rop(self, operator.rshift, other)

    # ---------------------------------------------------------
    # ~x (Bitwise Invert / Unární operátor)
    # ---------------------------------------------------------
    def __invert__(self):
        """Vrací novou instanci s hodnotou ~self.value."""
        try:
            return with_constant(self, self.meta.name_snake, ~self.value)
        except TypeError:
            return NotImplemented