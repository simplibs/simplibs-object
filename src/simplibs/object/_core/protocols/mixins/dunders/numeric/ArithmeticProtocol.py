from typing import Protocol, runtime_checkable, Any, Self
# Outers
from ...core_mixins import NodesDictsProtocol, SnapshotProtocol


@runtime_checkable
class ArithmeticProtocol(
    NodesDictsProtocol,
    SnapshotProtocol,
    Protocol
):
    """
    Protocol for the Arithmetic mixin.

    Guarantees a complete set of standard and right-hand arithmetic
    operators (+, -, *, /, //, %, **) with integrated safe type conversion.
    All operations are pure and return a new instance of the same type (Self).
    """

    # ----------------------------------------
    # Addition (+)
    # ----------------------------------------
    def __add__(self, other: Any) -> Self:
        """Returns a new instance with value (self.value + other)."""
        ...

    def __radd__(self, other: Any) -> Self:
        """Right-hand addition. Returns a new instance with value (other + self.value)."""
        ...

    # ----------------------------------------
    # Subtraction (-)
    # ----------------------------------------
    def __sub__(self, other: Any) -> Self:
        """Returns a new instance with value (self.value - other)."""
        ...

    def __rsub__(self, other: Any) -> Self:
        """Right-hand subtraction. Returns a new instance with value (other - self.value)."""
        ...

    # ----------------------------------------
    # Multiplication (*)
    # ----------------------------------------
    def __mul__(self, other: Any) -> Self:
        """Returns a new instance with value (self.value * other)."""
        ...

    def __rmul__(self, other: Any) -> Self:
        """Right-hand multiplication. Returns a new instance with value (other * self.value)."""
        ...

    # ----------------------------------------
    # True Division (/)
    # ----------------------------------------
    def __truediv__(self, other: Any) -> Self:
        """Returns a new instance with value (self.value / other)."""
        ...

    def __rtruediv__(self, other: Any) -> Self:
        """Right-hand true division. Returns a new instance with value (other / self.value)."""
        ...

    # ----------------------------------------
    # Floor Division (//)
    # ----------------------------------------
    def __floordiv__(self, other: Any) -> Self:
        """Returns a new instance with value (self.value // other)."""
        ...

    def __rfloordiv__(self, other: Any) -> Self:
        """Right-hand floor division. Returns a new instance with value (other // self.value)."""
        ...

    # ----------------------------------------
    # Modulo (%)
    # ----------------------------------------
    def __mod__(self, other: Any) -> Self:
        """Returns a new instance with value (self.value % other)."""
        ...

    def __rmod__(self, other: Any) -> Self:
        """Right-hand modulo. Returns a new instance with value (other % self.value)."""
        ...

    # ----------------------------------------
    # Power (**)
    # ----------------------------------------
    def __pow__(self, other: Any) -> Self:
        """Returns a new instance with value (self.value ** other)."""
        ...

    def __rpow__(self, other: Any) -> Self:
        """Right-hand exponentiation. Returns a new instance with value (other ** self.value)."""
        ...