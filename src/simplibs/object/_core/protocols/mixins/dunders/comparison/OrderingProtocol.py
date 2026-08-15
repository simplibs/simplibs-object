from typing import Protocol, runtime_checkable, Any
# Outers
from ...base_class import SimpleMixinProtocol


@runtime_checkable
class OrderingProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protocol for the Ordering mixin.

    Guarantees a complete set of comparison operators (ordering)
    between instances or between an instance and a raw value.
    """

    def __lt__(self, other: Any) -> bool:
        """Less than operator (<). Compares based on internal value."""
        ...

    def __le__(self, other: Any) -> bool:
        """Less than or equal operator (<=). Compares based on internal value."""
        ...

    def __gt__(self, other: Any) -> bool:
        """Greater than operator (>). Compares based on internal value."""
        ...

    def __ge__(self, other: Any) -> bool:
        """Greater than or equal operator (>=). Compares based on internal value."""
        ...