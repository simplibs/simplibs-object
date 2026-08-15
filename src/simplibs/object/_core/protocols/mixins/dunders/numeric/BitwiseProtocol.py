from typing import Protocol, runtime_checkable, Any, Self
# Outers
from ...core_mixins import NodesDictsProtocol, SnapshotProtocol


@runtime_checkable
class BitwiseProtocol(
    NodesDictsProtocol,
    SnapshotProtocol,
    Protocol
):
    """
    Protocol for the Bitwise mixin.

    Guarantees a complete set of bitwise operators (&, |, ^, <<, >>, ~).
    All operations are pure and return a new instance of the same type (Self).
    """

    # ----------------------------------------
    # AND Operator (&)
    # ----------------------------------------
    def __and__(self, other: Any) -> Self:
        """Returns a new instance with value (self.value & other)."""
        ...

    def __rand__(self, other: Any) -> Self:
        """Right-hand AND. Returns a new instance with value (other & self.value)."""
        ...

    # ----------------------------------------
    # OR Operator (|)
    # ----------------------------------------
    def __or__(self, other: Any) -> Self:
        """Returns a new instance with value (self.value | other)."""
        ...

    def __ror__(self, other: Any) -> Self:
        """Right-hand OR. Returns a new instance with value (other | self.value)."""
        ...

    # ----------------------------------------
    # XOR Operator (^)
    # ----------------------------------------
    def __xor__(self, other: Any) -> Self:
        """Returns a new instance with value (self.value ^ other)."""
        ...

    def __rxor__(self, other: Any) -> Self:
        """Right-hand XOR. Returns a new instance with value (other ^ self.value)."""
        ...

    # ----------------------------------------
    # LSHIFT Operator (<<)
    # ----------------------------------------
    def __lshift__(self, other: Any) -> Self:
        """Bitwise left shift. Returns a new instance with value (self.value << other)."""
        ...

    def __rlshift__(self, other: Any) -> Self:
        """Right-hand left shift. Returns a new instance with value (other << self.value)."""
        ...

    # ----------------------------------------
    # RSHIFT Operator (>>)
    # ----------------------------------------
    def __rshift__(self, other: Any) -> Self:
        """Bitwise right shift. Returns a new instance with value (self.value >> other)."""
        ...

    def __rrshift__(self, other: Any) -> Self:
        """Right-hand right shift. Returns a new instance with value (other >> self.value)."""
        ...

    # ----------------------------------------
    # INVERT Operator (~)
    # ----------------------------------------
    def __invert__(self) -> Self:
        """Unary bitwise inversion. Returns a new instance with value (~self.value)."""
        ...