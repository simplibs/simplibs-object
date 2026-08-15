from typing import Protocol, runtime_checkable
from collections.abc import Iterator
# Inners
from .CollectionBaseProtocol import CollectionBaseProtocol


@runtime_checkable
class IterableProtocol(
    CollectionBaseProtocol,
    Protocol
):
    """
    Protocol for the CollectionIterable mixin.

    Guarantees the iteration interface for composite objects, reverse iteration
    support, and extension of system introspection via dir().
    """

    def __iter__(self) -> Iterator[str]:
        """
        Returns an iterator over keys (name_snake) of all direct inner elements
        in the order defined by the blueprint.
        """
        ...

    def __reversed__(self) -> Iterator[str]:
        """
        Returns an iterator for traversing inner element keys in reverse order.
        """
        ...

    def __dir__(self) -> list[str]:
        """
        Returns a sorted list of all object attributes and methods,
        extended with the names of all inner elements (inners).
        """
        ...