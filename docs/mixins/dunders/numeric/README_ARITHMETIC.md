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
    Provides arithmetic operations (+, -, *, /, //, %, **) for SimpleObject.

    Supports:
    - atoms (constants)
    - composites (recomputes inners and owner values)

    Includes a lazy fallback type conversion:
    - if the operation fails, it attempts to convert the other operand to
      the type of the default value
    - the conversion is only performed if it is safe (e.g. int ->
      float/Decimal/Fraction)
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Compatibility declaration
    _only_types = Number

    # Slot definition
    __slots__ = ()

    # -------------------------
    # Methods - Addition (+)
    # -------------------------
    def __add__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Returns a new instance with the value self.value + other (with lazy fallback conversion)."""
        return execute_arithmetic_op(self, operator.add, other)

    def __radd__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Returns a new instance with the value other + self.value (with lazy fallback conversion)."""
        return execute_arithmetic_op(self, operator.add, other, is_reversed=True)

    # -------------------------
    # Methods - Subtraction (-)
    # -------------------------
    def __sub__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Returns a new instance with the value self.value - other (with lazy fallback conversion)."""
        return execute_arithmetic_op(self, operator.sub, other)

    def __rsub__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Returns a new instance with the value other - self.value (with lazy fallback conversion)."""
        return execute_arithmetic_op(self, operator.sub, other, is_reversed=True)

    # -------------------------
    # Methods - Multiplication (*)
    # -------------------------
    def __mul__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Returns a new instance with the value self.value * other (with lazy fallback conversion)."""
        return execute_arithmetic_op(self, operator.mul, other)

    def __rmul__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Returns a new instance with the value other * self.value (with lazy fallback conversion)."""
        return execute_arithmetic_op(self, operator.mul, other, is_reversed=True)

    # -------------------------
    # Methods - Division (/)
    # -------------------------
    def __truediv__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Returns a new instance with the value self.value / other (with lazy fallback conversion)."""
        return execute_arithmetic_op(self, operator.truediv, other)

    def __rtruediv__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Returns a new instance with the value other / self.value (with lazy fallback conversion)."""
        return execute_arithmetic_op(self, operator.truediv, other, is_reversed=True)

    # -------------------------
    # Methods - Floor division (//)
    # -------------------------
    def __floordiv__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Returns a new instance with the value self.value // other (with lazy fallback conversion)."""
        return execute_arithmetic_op(self, operator.floordiv, other)

    def __rfloordiv__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Returns a new instance with the value other // self.value (with lazy fallback conversion)."""
        return execute_arithmetic_op(self, operator.floordiv, other, is_reversed=True)

    # -------------------------
    # Methods - Modulo (%)
    # -------------------------
    def __mod__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Returns a new instance with the value self.value % other (with lazy fallback conversion)."""
        return execute_arithmetic_op(self, operator.mod, other)

    def __rmod__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Returns a new instance with the value other % self.value (with lazy fallback conversion)."""
        return execute_arithmetic_op(self, operator.mod, other, is_reversed=True)

    # -------------------------
    # Methods - Power (**)
    # -------------------------
    def __pow__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Returns a new instance with the value self.value ** other (with lazy fallback conversion)."""
        return execute_arithmetic_op(self, operator.pow, other)

    def __rpow__(
        self: "ArithmeticProtocol",
        other: Any
    ) -> "ArithmeticProtocol":
        """Returns a new instance with the value other ** self.value (with lazy fallback conversion)."""
        return execute_arithmetic_op(self, operator.pow, other, is_reversed=True)


_DESIGN_NOTES = """
# Arithmetic

## Purpose
Gives a SimpleObject the standard arithmetic operators (`+`, `-`, `*`,
`/`, `//`, `%`, `**`), including their reflected counterparts (`__radd__`
etc.), so numeric-valued instances behave like plain numbers in
expressions — `price + 10`, `10 + price`, and so on.

## Compatibility
- `_only_types = Number` — only applicable where `self.value` is expected
  to be numeric (`numbers.Number`), since every operation is delegated
  straight to Python's own arithmetic on the wrapped value.
- Works for both atoms and composites: composites recompute their inners
  and owner values as part of producing the result, atoms just
  recompute their own value.

## Logic
Every operator is a one-line call into the shared `execute_arithmetic_op`
helper, passing the matching `operator.*` function. The forward/reflected
pairs (`__add__`/`__radd__`, etc.) differ only in the `is_reversed=True`
flag, which tells the helper to compute `other <op> self.value` instead of
`self.value <op> other`.

The "lazy fallback conversion" mentioned in the class docstring lives
inside `execute_arithmetic_op`, not here: if the raw operation fails
(e.g. mixing `int` and `Decimal`), it attempts a safe conversion of the
other operand toward the type of the instance's default value before
giving up.

## Notes
- Every operator returns a **new instance**, never mutates in place —
  in-place arithmetic (`+=` etc.) is handled by the separate `Inplace`
  mixin, which is explicitly `_mutable_only`.
- All the actual arithmetic and conversion logic is centralized in
  `_utils.execute_arithmetic_op`, keeping this file a flat, readable list
  of operator wiring rather than duplicated logic per operator.
"""
