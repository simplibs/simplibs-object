from typing import Protocol, Any, runtime_checkable, TYPE_CHECKING
# Outers
from ..metadata import SimpleMetaProtocol
# Annotations
if TYPE_CHECKING:
    from ..metadata import SimpleMetadataLike


@runtime_checkable
class SimpleBaseProtocol(
    SimpleMetaProtocol,
    Protocol
):
    """
    Protocol for SimpleBase. Represents the fundamental interface
    shared across all constants and composite objects.
    """

    # --- Class interface (Overriding from SimpleMetaProtocol for explicit context) ---
    __metadata__: "SimpleMetadataLike"

    @property
    def meta(self) -> "SimpleMetadataLike":
        """Public access to the core class metadata."""
        ...