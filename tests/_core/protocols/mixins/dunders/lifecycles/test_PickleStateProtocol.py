from typing import Protocol, runtime_checkable, Any, TYPE_CHECKING
# Outers
from ...core_mixins import SerializationProtocol
# Annotations
if TYPE_CHECKING:
    from ....alias_typings import StateDict


@runtime_checkable
class PickleStateProtocol(
    SerializationProtocol,
    Protocol
):
    """
    Protocol for the PickleState mixin.

    Guarantees support for object state persistence and restoration (freezing/thawing)
    using the standard Python pickle protocol via dictionary representation.
    """

    def __getstate__(self) -> "StateDict":
        """
        Exports the complete current state of the instance as a clean dictionary.
        Internally leverages the to_dict() method to perform this operation.
        """
        ...

    def __setstate__(self, state: "StateDict") -> None:
        """
        Restores the internal state of the instance from the provided dictionary.
        Requires and invokes the from_dict() method, otherwise raises a TypeError.
        """
        ...

    # --- REQUIRED INTERFACE FOR PROPER MIXIN FUNCTIONALITY ---

    def from_dict(self, user_dict: "StateDict") -> Any:
        """
        Method that this mixin strictly requires on the target class
        for proper operation (implemented via Mutable/ImmutableSerialization).
        """
        ...