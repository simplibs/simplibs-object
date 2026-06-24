from typing import Protocol, runtime_checkable, Any, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ..metadata import SimpleBaseMetadataProtocol


@runtime_checkable
class SimpleInstanceBaseProtocol(Protocol):
    """
    Protokol pro InstanceBase. Společný jmenovatel a garant identity
    pro všechny instanční objekty (Atomy i Kompozice) v systému Simple.
    """

    def init_mixins(self) -> None:
        """Výchozí prázdná kotva pro reaktivní inicializaci mixinů."""
        ...

    def _before_update(self, new_value: Any) -> None:
        """Hook pro mixiny — spouští se před uložením nové hodnoty."""
        ...

    @property
    def meta(self) -> "SimpleBaseMetadataProtocol":
        """Veřejný přístup k metadatům třídy napřímo bez procházení MRO."""
        ...