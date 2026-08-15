from typing import Protocol, Any, runtime_checkable, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ..metadata import SimpleMetadataLike
    from ..instance.SimpleInstanceBaseProtocol import MixinsTuple


@runtime_checkable
class SimpleMetaProtocol(
    Protocol
):
    """
    Protocol representing the interface injected into all definition classes
    in the system by the SimpleMeta metaclass.
    """

    # Attribute where __new__ stores generated metadata
    __metadata__: "SimpleMetadataLike"

    @property
    def meta(self) -> "SimpleMetadataLike":
        """Public gateway for accessing class metadata."""
        ...

    def __call__(self, mixins: "MixinsTuple" = (), as_atom: bool = False) -> Any:
        """
        Allows calling the class itself as a function to create
        an instance of it with optional mixins.
        """
        ...

    # --- Explicit guarantees for text representation from SimpleMeta ---
    def __str__(self) -> str:
        """Returns the clean business name of the class (cls.__name__)."""
        ...

    def __repr__(self) -> str:
        """Technical representation of the definition class itself, including blueprint info."""
        ...