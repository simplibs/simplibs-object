from typing import Protocol, runtime_checkable
# Outers
from ...base_class import SimpleMixinProtocol


@runtime_checkable
class ValueDisplayProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protocol for the ValueDisplay mixin (formerly ValueDisplayRepr).

    Guarantees that the object represents itself externally as the raw value
    it wraps. Overrides technical representation (__repr__) for debugging
    and user-facing display (__str__) for text output.
    """

    def __repr__(self) -> str:
        """
        Returns a technical string representation for developers and logging
        in the format: ClassName(value_repr).
        """
        ...

    def __str__(self) -> str:
        """
        Returns the clean, human-readable value converted to a string.
        """
        ...