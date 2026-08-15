from typing import Protocol, runtime_checkable, Any, Callable
# Inners
from .ImmutableMethodsProtocol import ImmutableMethodsProtocol


@runtime_checkable
class ImmutableMethodsWithInnersProtocol(
    ImmutableMethodsProtocol,
    Protocol
):
    """
    Protocol for the ImmutableInnerMethods mixin.

    Guarantees the presence of dynamically generated immutable methods (setters)
    for individual inner elements (e.g., `obj.with_node(value)`).
    All such methods produce a new transformed instance (Self).
    """

    def __getattr__(self, name: str) -> Callable[[Any], Any]:
        """
        Dynamic fallback for accessing generated sub-node transformation methods
        (e.g., accessing `obj.with_engine`).

        Guarantees that invoking a method obtained this way results in a new,
        updated immutable instance of the same type (Self).
        """
        ...