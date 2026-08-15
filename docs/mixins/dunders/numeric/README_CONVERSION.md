from typing import TYPE_CHECKING
import math
from numbers import Number
# Outers
from ...base_class import SimpleMixin
#Inners
from ._utils import execute_conversion
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.dunders.numeric import ConversionProtocol


class Conversion(SimpleMixin):
    """
    Provides conversion dunders (int, float, complex, index, round,
    floor, ceil, trunc) for SimpleObject atoms and composites.

    These methods:
    - return native Python types (int, float, complex, ...)
    - do not return a SimpleObject
    - raise TypeError on an invalid conversion
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Compatibility declaration
    _only_types = Number

    # Slot definition
    __slots__ = ()

    # ----------------------------------------
    # Methods - INT / FLOAT / COMPLEX
    # ----------------------------------------
    def __int__(
        self: "ConversionProtocol"
    ) -> int:
        """Returns the native int(self.value)."""
        return execute_conversion(self, int)

    def __float__(
        self: "ConversionProtocol"
    ) -> float:
        """Returns the native float(self.value)."""
        return execute_conversion(self, float)

    def __complex__(
        self: "ConversionProtocol"
    ) -> complex:
        """Returns the native complex(self.value)."""
        return execute_conversion(self, complex)

    # ----------------------------------------
    # Methods - INDEX (for use in slice, range, etc.)
    # ----------------------------------------
    def __index__(
        self: "ConversionProtocol"
    ) -> int:
        """
        Returns the native int(self.value) for use in range(), slice,
        etc. Must return an exact int, otherwise Python raises TypeError.
        """
        value = self.value
        if not isinstance(value, int):
            raise TypeError(
                f"{self.meta.class_name} cannot be used as an index — "
                f"value must be int, not {type(value).__name__}."
            )
        return value

    # ----------------------------------------
    # Methods - ROUND
    # ----------------------------------------
    def __round__(
        self: "ConversionProtocol",
        n: int | None = None
    ) -> int | float:
        """Returns the native round(self.value, n)."""
        return (
            execute_conversion(self, round, n)
            if n is not None
            else execute_conversion(self, round)
        )

    # ----------------------------------------
    # Methods - FLOOR / CEIL / TRUNC
    # ----------------------------------------
    def __floor__(
        self: "ConversionProtocol"
    ) -> int:
        """Returns the native math.floor(self.value)."""
        return execute_conversion(self, math.floor)

    def __ceil__(
        self: "ConversionProtocol"
    ) -> int:
        """Returns the native math.ceil(self.value)."""
        return execute_conversion(self, math.ceil)

    def __trunc__(
        self: "ConversionProtocol"
    ) -> int:
        """Returns the native math.trunc(self.value)."""
        return execute_conversion(self, math.trunc)


_DESIGN_NOTES = """
# Conversion

## Purpose
Lets a SimpleObject be converted to native Python numeric types —
`int(obj)`, `float(obj)`, `complex(obj)`, `round(obj)`, `math.floor(obj)`,
etc. — and be used anywhere Python expects one of those, such as
`range(obj)` or slicing via `__index__`.

> For newcomers: unlike the other numeric mixins here, this one never
> returns a SimpleObject — every method returns a plain `int`/`float`/
> `complex`. That's the whole point: it's the "exit door" from the Simple
> ecosystem back into raw Python numbers.

## Compatibility
- `_only_types = Number` — every conversion assumes `self.value` is
  already numeric; a non-numeric value would fail these conversions
  anyway.
- Works for both atoms and composites — a composite with a well-defined
  numeric `.value` can be converted the same way an atom can.

## Logic
`__int__`, `__float__`, `__complex__`, `__round__`, `__floor__`,
`__ceil__`, `__trunc__` all delegate to the shared `execute_conversion`
helper, passing the matching native callable (`int`, `float`, `round`,
`math.floor`, ...).

`__index__` is the exception — implemented directly rather than through
`execute_conversion`, because Python's `__index__` protocol has a strict
requirement: it must return an *exact* `int`, or Python itself raises a
`TypeError`. This method enforces that up front with an explicit
`isinstance` check and a descriptive error, rather than letting a vague
failure surface later inside `range()` or a slice.

## Notes
- All conversions raise `TypeError` on failure — by design, never a
  silent `None` or a wrapped SimpleObject.
- `__round__`'s two call shapes (`round(obj)` vs `round(obj, n)`) are
  both explicitly forwarded, since Python calls `__round__` differently
  depending on whether `ndigits` was passed.
"""
