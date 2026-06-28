from typing import TYPE_CHECKING, Any
import operator
from numbers import Integral
# Outers
from ...core_mixins import NodesDicts, Snapshot
from ..._common.immutability import with_constant
# Inners
from ._utils import execute_bitwise_op
# Annotations
if TYPE_CHECKING:
    from ....protocols.mixins.dunders.numeric import BitwiseProtocol


class Bitwise(NodesDicts, Snapshot):
    """
    Poskytuje bitové operace (&, |, ^, <<, >>, ~) pro SimpleObject atomy.

    Vlastnosti:
    - funguje pouze pro atomy (konstanty)
    - funguje pouze pro integrální typy (int, vlastní integer-like typy)
    - operace jsou čisté → vrací novou instanci přes with_constant pipeline
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice určení
    _constant_only = True
    _only_types = Integral

    # Definice slotů
    __slots__ = ()

    # ----------------------------------------
    # Methods - & (Bitwise AND)
    # ----------------------------------------
    def __and__(
        self: "BitwiseProtocol",
        other: Any
    ) -> "BitwiseProtocol":
        """Vrací novou instanci s hodnotou self.value & other."""
        return execute_bitwise_op(self, operator.and_, other)

    def __rand__(
        self: "BitwiseProtocol",
        other: Any
    ) -> "BitwiseProtocol":
        """Vrací novou instanci s hodnotou other & self.value."""
        return execute_bitwise_op(self, operator.and_, other, is_reversed=True)

    # ----------------------------------------
    # Methods - | (Bitwise OR)
    # ----------------------------------------
    def __or__(
        self: "BitwiseProtocol",
        other: Any
    ) -> "BitwiseProtocol":
        """Vrací novou instanci s hodnotou self.value | other."""
        return execute_bitwise_op(self, operator.or_, other)

    def __ror__(
        self: "BitwiseProtocol",
        other: Any
    ) -> "BitwiseProtocol":
        """Vrací novou instanci s hodnotou other | self.value."""
        return execute_bitwise_op(self, operator.or_, other, is_reversed=True)

    # ----------------------------------------
    # Methods - ^ (Bitwise XOR)
    # ----------------------------------------
    def __xor__(
        self: "BitwiseProtocol",
        other: Any
    ) -> "BitwiseProtocol":
        """Vrací novou instanci s hodnotou self.value ^ other."""
        return execute_bitwise_op(self, operator.xor, other)

    def __rxor__(
        self: "BitwiseProtocol",
        other: Any
    ) -> "BitwiseProtocol":
        """Vrací novou instanci s hodnotou other ^ self.value."""
        return execute_bitwise_op(self, operator.xor, other, is_reversed=True)

    # ----------------------------------------
    # Methods - << (Bitwise Left Shift)
    # ----------------------------------------
    def __lshift__(
        self: "BitwiseProtocol",
        other: Any
    ) -> "BitwiseProtocol":
        """Vrací novou instanci s hodnotou self.value << other."""
        return execute_bitwise_op(self, operator.lshift, other)

    def __rlshift__(
        self: "BitwiseProtocol",
        other: Any
    ) -> "BitwiseProtocol":
        """Vrací novou instanci s hodnotou other << self.value."""
        return execute_bitwise_op(self, operator.lshift, other, is_reversed=True)

    # ----------------------------------------
    # Methods - >> (Bitwise Right Shift)
    # ----------------------------------------
    def __rshift__(
        self: "BitwiseProtocol",
        other: Any
    ) -> "BitwiseProtocol":
        """Vrací novou instanci s hodnotou self.value >> other."""
        return execute_bitwise_op(self, operator.rshift, other)

    def __rrshift__(
        self: "BitwiseProtocol",
        other: Any
    ) -> "BitwiseProtocol":
        """Vrací novou instanci s hodnotou other >> self.value."""
        return execute_bitwise_op(self, operator.rshift, other, is_reversed=True)

    # ----------------------------------------
    # Methods - ~x (Bitwise Invert / Unární operátor)
    # ----------------------------------------
    def __invert__(
        self: "BitwiseProtocol",
    ) -> Any:
        """Vrací novou instanci s hodnotou ~self.value."""
        try:
            value = ~self.value
            return with_constant(self, self.meta.name_snake, value)
        except TypeError:
            return NotImplemented