from typing import Protocol, Any, runtime_checkable, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ..metadata import SimpleMetadataLike


@runtime_checkable
class SimpleMetaProtocol(
    Protocol
):
    """
    Protokol reprezentující rozhraní, které metatřída SimpleMeta
    vštěpuje všem definičním třídám v systému.
    """

    # Atribut, do kterého __new__ ukládá vygenerovaná metadata
    __metadata__: "SimpleMetadataLike"

    @property
    def meta(self) -> "SimpleMetadataLike":
        """Veřejná brána pro přístup k metadatům třídy."""
        ...

    def __call__(self, mixins: tuple = (), as_atom: bool = False) -> Any:
        """
        Umožňuje samotnou třídu zavolat jako funkci a vytvořit tak
        její instanci s volitelnými mixiny.
        """
        ...