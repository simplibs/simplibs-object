from typing import Protocol, runtime_checkable, Any, Self
# Outers
from ...base_class import SimpleMixinProtocol


@runtime_checkable
class InplaceProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protocol for the Inplace mixin.

    Guarantees a set of in-place arithmetic operators (+=, -=, *=, /=, //=, %=, **=).
    All operations modify the object's value in place, trigger reactivity,
    and return the updated instance (Self).
    """

    # ----------------------------------------
    # In-place Addition (+=)
    # ----------------------------------------
    def __iadd__(self, other: Any) -> Self:
        """Modifies value in place: (self.value += other) and returns self."""
        ...

    # ----------------------------------------
    # In-place Subtraction (-=)
    # ----------------------------------------
    def __isub__(self, other: Any) -> Self:
        """Modifies value in place: (self.value -= other) and returns self."""
        ...

    # ----------------------------------------
    # In-place Multiplication (*=)
    # ----------------------------------------
    def __imul__(self, other: Any) -> Self:
        """Modifies value in place: (self.value *= other) and returns self."""
        ...

    # ----------------------------------------
    # In-place True Division (/=)
    # ----------------------------------------
    def __itruediv__(self, other: Any) -> Self:
        """Modifies value in place: (self.value /= other) and returns self."""
        ...

    # ----------------------------------------
    # In-place Floor Division (//=)
    # ----------------------------------------
    def __ifloordiv__(self, other: Any) -> Self:
        """Modifies value in place: (self.value //= other) and returns self."""
        ...

    # ----------------------------------------
    # In-place Modulo (%=)
    # ----------------------------------------
    def __imod__(self, other: Any) -> Self:
        """Modifies value in place: (self.value %= other) and returns self."""
        ...

    # ----------------------------------------
    # In-place Power (**=)
    # ----------------------------------------
    def __ipow__(self, other: Any) -> Self:
        """Modifies value in place: (self.value **= other) and returns self."""
        ...