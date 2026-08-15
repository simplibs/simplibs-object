import operator
from typing import TYPE_CHECKING, Any
from numbers import Number
# Outers
from ...base_class import SimpleMixin
#Inners
from ._utils import execute_inplace_op
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.dunders.numeric import InplaceProtocol


class Inplace(SimpleMixin):
    """
    Poskytuje in‑place aritmetické operace (+=, -=, *=, /=, //=, %=, **=)
    pro SimpleObject atomy a mutable instance.

    Operace:
    - mění hodnotu instance přes self.value = ...
    - aktivují validaci a reaktivitu
    - vrací self
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice určení
    _mutable_only = True
    _only_types = Number

    # Definice slotů
    __slots__ = ()

    # ----------------------------------------
    # Methods - Operátory (+=, -=, *=, /=, //=, %=, **=)
    # ----------------------------------------
    def __iadd__(
        self: "InplaceProtocol",
        other: Any
    ) -> "InplaceProtocol":
        """In‑place: self.value += other."""
        return execute_inplace_op(self, operator.add, other)

    def __isub__(
        self: "InplaceProtocol",
        other: Any
    ) -> "InplaceProtocol":
        """In‑place: self.value -= other."""
        return execute_inplace_op(self, operator.sub, other)

    def __imul__(
        self: "InplaceProtocol",
        other: Any
    ) -> "InplaceProtocol":
        """In‑place: self.value *= other."""
        return execute_inplace_op(self, operator.mul, other)

    def __itruediv__(
        self: "InplaceProtocol",
        other: Any
    ) -> "InplaceProtocol":
        """In‑place: self.value /= other."""
        return execute_inplace_op(self, operator.truediv, other)

    def __ifloordiv__(
        self: "InplaceProtocol",
        other: Any
    ) -> "InplaceProtocol":
        """In‑place: self.value //= other."""
        return execute_inplace_op(self, operator.floordiv, other)

    def __imod__(
        self: "InplaceProtocol",
        other: Any
    ) -> "InplaceProtocol":
        """In‑place: self.value %= other."""
        return execute_inplace_op(self, operator.mod, other)

    def __ipow__(
        self: "InplaceProtocol",
        other: Any
    ) -> "InplaceProtocol":
        """In‑place: self.value **= other."""
        return execute_inplace_op(self, operator.pow, other)