from typing import Protocol, Any, runtime_checkable, TYPE_CHECKING
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
    Protocol for an Atom instance (the result of make_atom_class).
    Combines the instance foundation (InstanceBase) with the template behavior (SimpleConstantProtocol).
    """

    # --- Internal state (slots) ---
    _value: Any
    _owner: "SimpleInstanceLike"
    _locked: bool

    # --- Internal methods ---
    def _root_value_setter(self, new_value: Any, recalculate_up: bool) -> None:
        """Internal mechanism for safely setting the root value."""
        ...

    # --- Public properties ---
    @property
    def value(self) -> Any:
        """Current normalized value of this atom."""
        ...

    @value.setter
    def value(self, new_value: Any) -> None:
        """Sets a new value for the atom (available in mutable mode)."""
        ...

    @property
    def owner(self) -> "SimpleInstanceLike":
        """Reference to the parent composition (if it exists)."""
        ...