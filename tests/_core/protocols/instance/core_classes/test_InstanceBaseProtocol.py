from typing import Protocol, runtime_checkable, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ...metadata import SimpleMetadataLike
    from ...classes import SimpleClassLike


@runtime_checkable
class InstanceBaseProtocol(
    Protocol
):
    """
    Protocol for InstanceBase. The common denominator and identity guarantor
    for all instance objects (Atoms and Composites) in the Simple system.
    """

    def init_mixins(self) -> None:
        """Default empty anchor for reactive mixin initialization."""
        ...

    @property
    def meta(self) -> "SimpleMetadataLike":
        """Public access to class metadata directly without traversing MRO."""
        ...

    __class__: "SimpleClassLike"