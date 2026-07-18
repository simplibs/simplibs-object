from typing import Protocol, Any, runtime_checkable, TYPE_CHECKING
# Outers
from ...classes import SimpleObjectProtocol
# Inners
from .AtomInstanceProtocol import AtomInstanceProtocol
# Anotattions
if TYPE_CHECKING:
    from ...instance import SimpleInstanceLike


@runtime_checkable
class CompositeInstanceProtocol(
    AtomInstanceProtocol,
    SimpleObjectProtocol,
    Protocol
):
    """
    Protokol pro instanci Kompozice (výsledek make_composite_class).
    Slučuje instanční chování Atomu s pokročilými třídními metodami šablony Object.
    """

    # --- Interní metody kompozice ---
    def _recalculate_self(self) -> None:
        """Spustí přepočet hodnoty této kompozice na základě jejích inners."""
        ...

    def _recalculate_inners(self) -> None:
        """Rozdistribuuje novou hodnotu do vnitřních prvků."""
        ...

    # --- Dynamické rozhraní pro vnitřní prvky ---
    def __getattr__(self, name: str) -> "SimpleInstanceLike":
        """
        Dynamický přístup k vnitřním prvkům (inners) skrze vygenerované properties.
        Vrací buď pod-kompozici nebo atom.
        """
        ...