from typing import Protocol, runtime_checkable, Any
# Outers
from ...base_class import SimpleMixinProtocol


@runtime_checkable
class EqualityProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protocol for the Equality mixin.

    Guarantees the ability to compare instances for equality (value and object identity)
    and provides a safe, dynamic hashing strategy responsive to mutability state.
    """

    def __eq__(self, other: Any) -> bool:
        """
        Compares the instance with another object for equality.
        Returns True if values (and potentially blueprints) match, False otherwise.
        """
        ...

    def __hash__(self) -> int:
        """
        Returns a unique numerical hash for the instance.
        For mutable objects, generates a hash from identity id(self);
        for immutable objects, from the value hash(self.value).
        """
        ...