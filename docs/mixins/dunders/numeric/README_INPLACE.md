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
    Provides in-place arithmetic operations (+=, -=, *=, /=, //=, %=, **=)
    for SimpleObject atoms and mutable instances.

    Operations:
    - change the instance's value via self.value = ...
    - trigger validation and reactivity
    - return self
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Compatibility declaration
    _mutable_only = True
    _only_types = Number

    # Slot definition
    __slots__ = ()

    # ----------------------------------------
    # Methods - Operators (+=, -=, *=, /=, //=, %=, **=)
    # ----------------------------------------
    def __iadd__(
        self: "InplaceProtocol",
        other: Any
    ) -> "InplaceProtocol":
        """In-place: self.value += other."""
        return execute_inplace_op(self, operator.add, other)

    def __isub__(
        self: "InplaceProtocol",
        other: Any
    ) -> "InplaceProtocol":
        """In-place: self.value -= other."""
        return execute_inplace_op(self, operator.sub, other)

    def __imul__(
        self: "InplaceProtocol",
        other: Any
    ) -> "InplaceProtocol":
        """In-place: self.value *= other."""
        return execute_inplace_op(self, operator.mul, other)

    def __itruediv__(
        self: "InplaceProtocol",
        other: Any
    ) -> "InplaceProtocol":
        """In-place: self.value /= other."""
        return execute_inplace_op(self, operator.truediv, other)

    def __ifloordiv__(
        self: "InplaceProtocol",
        other: Any
    ) -> "InplaceProtocol":
        """In-place: self.value //= other."""
        return execute_inplace_op(self, operator.floordiv, other)

    def __imod__(
        self: "InplaceProtocol",
        other: Any
    ) -> "InplaceProtocol":
        """In-place: self.value %= other."""
        return execute_inplace_op(self, operator.mod, other)

    def __ipow__(
        self: "InplaceProtocol",
        other: Any
    ) -> "InplaceProtocol":
        """In-place: self.value **= other."""
        return execute_inplace_op(self, operator.pow, other)


_DESIGN_NOTES = """
# Inplace

## Purpose
Gives a mutable SimpleObject the in-place arithmetic operators (`+=`,
`-=`, `*=`, `/=`, `//=`, `%=`, `**=`), so a variable holding a mutable
instance can be updated in place, the same way plain numbers are.

## Compatibility
- `_mutable_only = True` — this is the key difference from `Arithmetic`.
  Where `+` always returns a new instance, `+=` here genuinely mutates
  `self.value`, which is only a coherent operation on a mutable instance.
  On an immutable instance, `+=` would need to rebind the variable to a
  new object anyway, which is exactly what `Arithmetic.__add__` already
  provides — so `Inplace` doesn't need to (and must not) apply there.
- `_only_types = Number` — same reasoning as `Arithmetic`: the operators
  only make sense on numeric values.

## Logic
Each operator delegates to the shared `execute_inplace_op` helper with
the matching `operator.*` function. Unlike `Arithmetic`'s helper, this
one is expected to:
1. Compute the new value.
2. Assign it via `self.value = ...`, which routes through the normal
   validation and reactivity pipeline (so a bad in-place update is
   rejected the same way a bad direct assignment would be).
3. Return `self`, satisfying Python's expectation that `__iadd__` etc.
   return the (possibly same) object to rebind the name to.

## Notes
- No reflected variants exist for in-place operators in Python (there's
  no `__riadd__`) — this mixin only needs the forward set.
- Choosing between `Arithmetic` and `Inplace` mixins on a class is really
  choosing between "always get a new instance" and "mutate the existing
  one" — a class can have both, since `+` and `+=` are independent
  protocols, but `Inplace` alone would leave plain `+` undefined.
"""
