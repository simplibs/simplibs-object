from typing import TYPE_CHECKING, Any
import operator
from numbers import Integral
# Outers
from ...core_mixins import NodesDicts, Snapshot
from ..._common_logic.immutability import with_constant
# Inners
from ._utils import execute_bitwise_op
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.dunders.numeric import BitwiseProtocol


class Bitwise(NodesDicts, Snapshot):
    """
    Provides bitwise operations (&, |, ^, <<, >>, ~) for SimpleObject
    atoms.

    Properties:
    - works only for atoms (constants)
    - works only for integral types (int, custom integer-like types)
    - operations are pure -> return a new instance via the with_constant
      pipeline
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Compatibility declaration
    _constant_only = True
    _only_types = Integral

    # Slot definition
    __slots__ = ()

    # ----------------------------------------
    # Methods - & (Bitwise AND)
    # ----------------------------------------
    def __and__(
        self: "BitwiseProtocol",
        other: Any
    ) -> "BitwiseProtocol":
        """Returns a new instance with the value self.value & other."""
        return execute_bitwise_op(self, operator.and_, other)

    def __rand__(
        self: "BitwiseProtocol",
        other: Any
    ) -> "BitwiseProtocol":
        """Returns a new instance with the value other & self.value."""
        return execute_bitwise_op(self, operator.and_, other, is_reversed=True)

    # ----------------------------------------
    # Methods - | (Bitwise OR)
    # ----------------------------------------
    def __or__(
        self: "BitwiseProtocol",
        other: Any
    ) -> "BitwiseProtocol":
        """Returns a new instance with the value self.value | other."""
        return execute_bitwise_op(self, operator.or_, other)

    def __ror__(
        self: "BitwiseProtocol",
        other: Any
    ) -> "BitwiseProtocol":
        """Returns a new instance with the value other | self.value."""
        return execute_bitwise_op(self, operator.or_, other, is_reversed=True)

    # ----------------------------------------
    # Methods - ^ (Bitwise XOR)
    # ----------------------------------------
    def __xor__(
        self: "BitwiseProtocol",
        other: Any
    ) -> "BitwiseProtocol":
        """Returns a new instance with the value self.value ^ other."""
        return execute_bitwise_op(self, operator.xor, other)

    def __rxor__(
        self: "BitwiseProtocol",
        other: Any
    ) -> "BitwiseProtocol":
        """Returns a new instance with the value other ^ self.value."""
        return execute_bitwise_op(self, operator.xor, other, is_reversed=True)

    # ----------------------------------------
    # Methods - << (Bitwise Left Shift)
    # ----------------------------------------
    def __lshift__(
        self: "BitwiseProtocol",
        other: Any
    ) -> "BitwiseProtocol":
        """Returns a new instance with the value self.value << other."""
        return execute_bitwise_op(self, operator.lshift, other)

    def __rlshift__(
        self: "BitwiseProtocol",
        other: Any
    ) -> "BitwiseProtocol":
        """Returns a new instance with the value other << self.value."""
        return execute_bitwise_op(self, operator.lshift, other, is_reversed=True)

    # ----------------------------------------
    # Methods - >> (Bitwise Right Shift)
    # ----------------------------------------
    def __rshift__(
        self: "BitwiseProtocol",
        other: Any
    ) -> "BitwiseProtocol":
        """Returns a new instance with the value self.value >> other."""
        return execute_bitwise_op(self, operator.rshift, other)

    def __rrshift__(
        self: "BitwiseProtocol",
        other: Any
    ) -> "BitwiseProtocol":
        """Returns a new instance with the value other >> self.value."""
        return execute_bitwise_op(self, operator.rshift, other, is_reversed=True)

    # ----------------------------------------
    # Methods - ~x (Bitwise Invert / Unary operator)
    # ----------------------------------------
    def __invert__(
        self: "BitwiseProtocol",
    ) -> Any:
        """Returns a new instance with the value ~self.value."""
        try:
            value = ~self.value
            return with_constant(self, self.meta.name_snake, value)
        except TypeError:
            return NotImplemented


_DESIGN_NOTES = """
# Bitwise

## Purpose
Gives a SimpleObject atom the standard bitwise operators (`&`, `|`, `^`,
`<<`, `>>`, `~`), including reflected forms, so integer-valued constants
behave like plain `int` in bit-manipulation code — flags, masks, bit
shifting, etc.

## Compatibility
- `_constant_only = True` — bitwise operations only make sense on a
  single scalar value, not on a composite's tree of inners, so this
  mixin is restricted to atoms.
- `_only_types = Integral` — narrower than `Arithmetic`'s `Number`: bit
  operations are only meaningful on integral types (`int` and
  integer-like custom types), not on floats.

## Logic
`&`, `|`, `^`, `<<`, `>>` all follow the same pattern as `Arithmetic`:
delegate to `execute_bitwise_op` with the matching `operator.*` function,
using `is_reversed=True` for the reflected variants.

`__invert__` (`~x`) is handled separately since it's unary and has no
reflected counterpart: it computes `~self.value` directly and wraps the
result via `with_constant`, catching `TypeError` and returning
`NotImplemented` if the value doesn't support inversion.

## Notes
- "Operations are pure" — every operator returns a **new** instance via
  the `with_constant` pipeline rather than mutating in place, consistent
  with `Arithmetic`.
- Deliberately narrower than `Arithmetic` in two ways at once
  (`_constant_only` + `Integral`) — this is what distinguishes "a
  constant that behaves like an int with bit ops" from "a value that
  supports general math," which composites and floats can still get via
  `Arithmetic` alone.
"""
