from typing import Protocol, Any, runtime_checkable, TYPE_CHECKING
# Outers
from ..classes import SimpleConstantProtocol
# Inners
from .SimpleInstanceBaseProtocol import SimpleInstanceBaseProtocol
# Annotations
if TYPE_CHECKING:
    from ..metadata import SimpleConstantMetadataProtocol
    from .SimpleCompositeInstanceProtocol import SimpleCompositeInstanceProtocol


@runtime_checkable
class SimpleAtomInstanceProtocol(
    SimpleInstanceBaseProtocol,
    SimpleConstantProtocol,
    Protocol
):
    """
    Protokol pro instanci Atomu (výsledek make_atom_class).
    Slučuje instanční základ (InstanceBase) s chováním šablony (SimpleConstantProtocol).
    """

    # --- KOVARIANTNÍ PŘEPIS METADAT (Upřesňujeme na konstantní metadata) ---
    @property
    def meta(self) -> "SimpleConstantMetadataProtocol":
        """Přístup k rozšířeným konstantním metadatům třídy."""
        ...

    # --- Interní stav (slots) ---
    _value: Any
    _owner: "SimpleCompositeInstanceProtocol | None"

    # --- Interní metody ---
    def _root_value_setter(self, new_value: Any) -> None:
        """Interní mechanismus pro bezpečné nastavení hodnoty kořene."""
        ...

    # --- Veřejné properties ---
    @property
    def value(self) -> Any:
        """Aktuální normalizovaná hodnota tohoto atomu."""
        ...

    @property
    def owner(self) -> "SimpleCompositeInstanceProtocol | None":
        """Reference na nadřazenou kompozici (pokud existuje)."""
        ...