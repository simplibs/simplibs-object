from typing import Protocol, runtime_checkable, TYPE_CHECKING
# Outers
from ..base_class import SimpleMixinProtocol
# Annotations
if TYPE_CHECKING:
    from ...instance import SimpleInstanceLike


@runtime_checkable
class InnersPropertyProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protocol for the InnersProperty mixin.

    Indicates that a composite instance was dynamically extended with properties
    enabling convenient direct access to its inner elements (inners)
    based on the blueprint definition.
    """

    # The mixin itself has no slots; properties are generated at runtime.

    def __getattr__(self, name: str) -> "SimpleInstanceLike":
        """
        Dynamic fallback for accessing generated inner element properties.

        Guarantees that any dynamically retrieved element (sub-composite or atom)
        conforms to the base instance interface.
        """
        ...