from typing import Protocol, Any, runtime_checkable, TYPE_CHECKING
# Outers
from ...classes import SimpleObjectProtocol
# Inners
from .AtomInstanceProtocol import AtomInstanceProtocol
# Annotations
if TYPE_CHECKING:
    from ...instance import SimpleInstanceLike


@runtime_checkable
class CompositeInstanceProtocol(
    AtomInstanceProtocol,
    SimpleObjectProtocol,
    Protocol
):
    """
    Protocol for a Composite instance (the result of make_composite_class).
    Combines the instance behavior of an Atom with the advanced class methods of the Object template.
    """

    # --- Internal composition methods ---
    def _recalculate_self(self) -> None:
        """Triggers recalculation of this composition's value based on its inners."""
        ...

    def _recalculate_inners(self) -> None:
        """Distributes a new value down to the inner elements."""
        ...

    # --- Dynamic interface for inner elements ---
    def __getattr__(self, name: str) -> "SimpleInstanceLike":
        """
        Dynamic access to inner elements (inners) via generated properties.
        Returns either a sub-composition or an atom.
        """
        ...