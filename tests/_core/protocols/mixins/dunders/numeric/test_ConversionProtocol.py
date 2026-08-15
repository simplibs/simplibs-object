from typing import Protocol, runtime_checkable, Any
# Outers
from ...base_class import SimpleMixinProtocol


@runtime_checkable
class ConversionProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protocol for the Conversion mixin.

    Guarantees a set of standard conversion and mathematical methods
    that convert the object's internal value into native Python types.
    """

    # ----------------------------------------
    # Basic Type Conversions
    # ----------------------------------------
    def __int__(self) -> int:
        """Returns a native int derived from the object's value."""
        ...

    def __float__(self) -> float:
        """Returns a native float derived from the object's value."""
        ...

    def __complex__(self) -> complex:
        """Returns a native complex derived from the object's value."""
        ...

    def __index__(self) -> int:
        """
        Returns a pure int for using the object as an index (slice, range, etc.).
        Must return a strict int, otherwise Python raises a TypeError.
        """
        ...

    # ----------------------------------------
    # Mathematical Truncation and Rounding
    # ----------------------------------------
    def __round__(self, n: int | None = None) -> int | float:
        """Returns a native rounded value to 'n' decimal places."""
        ...

    def __floor__(self) -> int:
        """Returns a native integer rounded down (math.floor)."""
        ...

    def __ceil__(self) -> int:
        """Returns a native integer rounded up (math.ceil)."""
        ...

    def __trunc__(self) -> int:
        """Returns a native integer truncated toward zero (math.trunc)."""
        ...