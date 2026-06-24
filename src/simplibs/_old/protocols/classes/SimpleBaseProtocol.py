from typing import Protocol, Any, runtime_checkable, TYPE_CHECKING
# Inners
from .SimpleMetaProtocol import SimpleMetaProtocol
# Annotations
if TYPE_CHECKING:
    from ..metadata import SimpleBaseMetadataProtocol


@runtime_checkable
class SimpleBaseProtocol(SimpleMetaProtocol, Protocol):
    """
    Protokol pro SimpleBase. Reprezentuje základní rozhraní
    společné pro všechny konstanty i kompozitní objekty.
    """

    # --- Třídní rozhraní (Přepisujeme z SimpleMetaProtocol pro jasný kontext) ---
    __metadata__: "SimpleBaseMetadataProtocol"

    @property
    def meta(self) -> "SimpleBaseMetadataProtocol":
        """Veřejný přístup k základním metadatům třídy."""
        ...

    # --- Vnitřní rozhraní třídy ---
    @classmethod
    def _log_outcome(cls, outcome: Any) -> None:
        """
        Třídní hook pro případný loger výsledků metod.
        Volá se z vnitřních procesů.
        """
        ...