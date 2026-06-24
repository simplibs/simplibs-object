from typing import Protocol, Any, runtime_checkable, TYPE_CHECKING
# Outers
from ..classes import SimpleObjectProtocol
# Inners
from .SimpleAtomInstanceProtocol import SimpleAtomInstanceProtocol
# Anotattions
if TYPE_CHECKING:
    from ..metadata import SimpleObjectMetadataProtocol
    from ..types import SimpleInstanceType


@runtime_checkable
class SimpleCompositeInstanceProtocol(
    SimpleAtomInstanceProtocol,
    SimpleObjectProtocol,
    Protocol
):
    """
    Protokol pro instanci Kompozice (výsledek make_composite_class).
    Slučuje instanční chování Atomu s pokročilými třídními metodami šablony Object.
    """

    # --- KOVARIANTNÍ PŘEPIS METADAT (Upřesňujeme na kompozitní metadata) ---
    @property
    def meta(self) -> "SimpleObjectMetadataProtocol":
        """Přístup k nejvyšší úrovni kompozitních metadat třídy."""
        ...

    # --- Interní metody kompozice ---
    def _recalculate_self(self) -> None:
        """Spustí přepočet hodnoty této kompozice na základě jejích inners."""
        ...

    def _recalculate_inners(self, decomposed_value: Any) -> None:
        """Rozdistribuuje novou hodnotu do vnitřních prvků."""
        ...

    # --- Dynamické rozhraní pro vnitřní prvky ---
    def __getattr__(self, name: str) -> "SimpleInstanceType":
        """
        Dynamický přístup k vnitřním prvkům (inners) skrze vygenerované properties.
        Vrací buď pod-kompozici nebo atom.
        """
        ...