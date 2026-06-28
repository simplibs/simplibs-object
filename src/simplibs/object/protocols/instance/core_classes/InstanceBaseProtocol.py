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
    Protokol pro InstanceBase. Společný jmenovatel a garant identity
    pro všechny instanční objekty (Atomy i Kompozice) v systému Simple.
    """

    def init_mixins(self) -> None:
        """Výchozí prázdná kotva pro reaktivní inicializaci mixinů."""
        ...

    @property
    def meta(self) -> "SimpleMetadataLike":
        """Veřejný přístup k metadatům třídy napřímo bez procházení MRO."""
        ...

    __class__: "SimpleClassLike"