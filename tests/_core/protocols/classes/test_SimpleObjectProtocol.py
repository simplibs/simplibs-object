from typing import Protocol, Any, runtime_checkable, TYPE_CHECKING
# Outers
from ..methods import LogicSignature, P, R
# Inners
from .SimpleConstantProtocol import SimpleConstantProtocol
# Annotations
if TYPE_CHECKING:
    from ..metadata import SimpleMetadataLike
    from ..alias_typings import InnersTuple


@runtime_checkable
class SimpleObjectProtocol(
    SimpleConstantProtocol,
    Protocol
):
    """
    Protocol for SimpleObject. Represents the full interface of composite classes (Nodes),
    including inner elements, transformation logic, and advanced dynamic typing.
    """

    # --- INTERNAL INTERFACE (Defined by the user when creating the composition) ---
    _inners: "InnersTuple"

    @classmethod
    def _logic(cls, *args: P.args, **kwargs: P.kwargs) -> R:
        """Required computation method for the composition that determines its signature."""
        ...

    @classmethod
    def _decompose(cls, value: Any) -> Any:
        """Optional method for decomposing the main value."""
        ...

    # --- EXTERNAL INTERFACE (Methods added/available for working with the composition) ---
    @classmethod
    def calculate_value(cls: LogicSignature[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
        """
        Dynamically calculates the composition value and uses ParamSpec
        to propagate specific parameters from the custom '_logic' method.
        """
        ...

    @classmethod
    def decompose_value(cls, value: Any) -> Any:
        """Decomposes the main value into inner components."""
        ...

    __mro__: Any
    meta: "SimpleMetadataLike"