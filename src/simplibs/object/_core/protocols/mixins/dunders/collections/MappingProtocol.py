from typing import Protocol, runtime_checkable, Any
# Inners
from .CollectionBaseProtocol import CollectionBaseProtocol


@runtime_checkable
class MappingProtocol(
    CollectionBaseProtocol,
    Protocol
):
    """
    Protocol for the CollectionMapping mixin.

    Guarantees the dictionary (Mapping) interface for composite objects,
    including reading, writing, key containment checks, and safe lookups.
    """

    def __len__(self) -> int:
        """Returns the total count of direct inner elements (inners) in the composite."""
        ...

    def __contains__(self, key: str) -> bool:
        """Returns True if the composite contains an inner element with the given key (name_snake)."""
        ...

    def __missing__(self, key: str) -> None:
        """
        Raises a detailed KeyError with context about available keys
        when the requested inner element does not exist in the composite.
        """
        ...

    def __getitem__(self, key: str) -> Any:
        """
        Returns the value of an inner element by its key.
        If the key does not exist, delegates handling to __missing__.
        """
        ...

    def get(self, key: str, default: Any = None) -> Any:
        """
        Safely returns the value of an inner element by key.
        If the key does not exist, returns the specified default value.
        """
        ...

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Sets a new value for the inner element specified by key.
        Raises a TypeError on immutable objects or a KeyError if the key does not exist.
        """
        ...