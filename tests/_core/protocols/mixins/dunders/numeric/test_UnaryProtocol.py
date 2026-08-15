from typing import Protocol, runtime_checkable, Self
# Outers
from ...core_mixins import NodesDictsProtocol, SnapshotProtocol


@runtime_checkable
class UnaryProtocol(
    NodesDictsProtocol,
    SnapshotProtocol,
    Protocol
):
    """
    Protocol for the Unary mixin.

    Guarantees a set of unary numerical operators (-x, +x, abs(x)).
    All operations are pure and return a new instance of the same type (Self).
    """

    # ----------------------------------------
    # Unary Sign Operations
    # ----------------------------------------
    def __neg__(self) -> Self:
        """Mathematical negation. Returns a new instance with value (-self.value)."""
        ...

    def __pos__(self) -> Self:
        """Unary plus. Returns a new instance with value (+self.value)."""
        ...

    # ----------------------------------------
    # Absolute Value
    # ----------------------------------------
    def __abs__(self) -> Self:
        """Returns a new instance with absolute value: abs(self.value)."""
        ...