from typing import TYPE_CHECKING
import operator
from numbers import Number
# Outers
from ...core_mixins import NodesDicts, Snapshot
# Inners
from ._utils import execute_unary_op
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.dunders.numeric import UnaryProtocol


class Unary(NodesDicts, Snapshot):
    """
    Provides unary numeric operations (-x, +x, abs(x)) for SimpleObject.

    Supports:
    - atoms (constants)
    - composites (recomputes inner inners and owner values)

    Includes a lazy fallback type conversion:
    - if the operation fails, it attempts to convert the value to the
      type of the default value
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

    # ----------------------------------------
    # Methods - Unary operators (-x, +x, abs(x))
    # ----------------------------------------
    def __neg__(
        self: "UnaryProtocol"
    ) -> "UnaryProtocol":
        """Returns a new instance with the value -self.value."""
        return execute_unary_op(self, operator.neg)

    def __pos__(
        self: "UnaryProtocol"
    ) -> "UnaryProtocol":
        """Returns a new instance with the value +self.value."""
        return execute_unary_op(self, operator.pos)

    def __abs__(
        self: "UnaryProtocol"
    ) -> "UnaryProtocol":
        """Returns a new instance with the value abs(self.value)."""
        return execute_unary_op(self, abs)


_DESIGN_NOTES = """
# Unary

## Purpose
Gives a SimpleObject the unary numeric operators — `-x`, `+x`, `abs(x)` —
so numeric-valued instances support the same single-operand math Python
numbers do.

## Compatibility
- `_only_types = Number` — same reasoning as `Arithmetic`: every
  operation is delegated to Python's own math on `self.value`.
- Works for both atoms and composites, recomputing inners and owner
  values on composites the same way `Arithmetic` does.

## Logic
All three operators are one-line calls into the shared
`execute_unary_op` helper, passing `operator.neg`, `operator.pos`, or the
`abs` builtin. As with `Arithmetic`, the lazy fallback type conversion
(trying a safe type conversion if the raw operation fails) lives inside
that shared helper, not in this file.

## Notes
- Every operator returns a **new instance**, consistent with
  `Arithmetic` — there's no in-place unary form since `-x` and `+x`
  don't have in-place equivalents in Python to begin with.
- Deliberately separate from `Arithmetic` even though both share the
  same `_utils` module and `Number` restriction — unary and binary
  operators are independent Python protocols, so a class could in
  principle mix in one without the other.
"""
