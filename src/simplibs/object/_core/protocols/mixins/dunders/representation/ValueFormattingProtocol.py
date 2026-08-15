from typing import Protocol, runtime_checkable, Any
# Outers
from ...base_class import SimpleMixinProtocol


@runtime_checkable
class ValueFormattingProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protocol for the Conversion mixin (formerly Representation).

    Guarantees support for f-string formatting using metadata masks,
    along with native conversion of the object to bytes and bool based on its internal value.
    """

    def format(self, pattern: str | None = None) -> str:
        """
        Formats the internal value of the instance according to the specified pattern
        or mask defined in the metadata.
        """
        ...

    def __format__(self, format_spec: str = "") -> str:
        """
        Support for f-string formatting. Enables f"{obj:pattern}" syntax.
        """
        ...

    def __bytes__(self) -> bytes:
        """
        Native conversion of the instance's internal value to bytes.
        Raises TypeError for incompatible types.
        """
        ...

    def __bool__(self) -> bool:
        """
        Returns the truth value of the object evaluated from its internal value.
        """
        ...