from typing import Protocol, Any, runtime_checkable, TYPE_CHECKING
from simplibs.sentinels import UnsetType
# Outers
from ...classes import SimpleConstantProtocol
# Inners
from .InstanceBaseProtocol import InstanceBaseProtocol
# Annotations
if TYPE_CHECKING:
    from ...instance import SimpleInstanceLike


@runtime_checkable
class AtomInstanceProtocol(
    InstanceBaseProtocol,
    SimpleConstantProtocol,
    Protocol
):
    """
    Protokol pro instanci Atomu (výsledek make_atom_class).
    Slučuje instanční základ (InstanceBase) s chováním šablony (SimpleConstantProtocol).
    """

    # --- Interní stav (slots) ---
    _value: Any
    _owner: "SimpleInstanceLike | UnsetType"
    _locked: bool

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
    def owner(self) -> "SimpleInstanceLike | UnsetType":
        """Reference na nadřazenou kompozici (pokud existuje)."""
        ...