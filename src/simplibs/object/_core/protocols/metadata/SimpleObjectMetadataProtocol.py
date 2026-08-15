from typing import Protocol, runtime_checkable, TYPE_CHECKING, Callable
# Inners
from .SimpleConstantMetadataProtocol import SimpleConstantMetadataProtocol
# Annotations
if TYPE_CHECKING:
    from ..instance.core_classes import CompositeInstanceProtocol
    from ..alias_typings import NamesTuple, InnersMap, InnersTuple


@runtime_checkable
class SimpleObjectMetadataProtocol(
    SimpleConstantMetadataProtocol,
    Protocol
):
    """
    Protocol for composite node class metadata specifications.

    Manages structural inner elements, lookup mapping, parameter alignment,
    and bound methods (_logic, _decompose, _validate).
    Exposes lazy-loaded gateways (composite_class_mutable, composite_class_immutable)
    for synthesising composite runtime instance classes on demand.
    """

    # 1. User-provided data
    inners: "InnersTuple"
    logic: Callable
    decompose: Callable

    # 2. Maps for inner elements
    inners_params_name: "NamesTuple"
    inners_map: "InnersMap"

    # 3. Public interface
    is_decomposeable: bool

    # 4. Cache interface
    _composite_class_mutable: "CompositeInstanceProtocol"
    _composite_class_immutable: "CompositeInstanceProtocol"

    # 5. Cache for instance classes (defined as read-only properties)
    @property
    def composite_class_mutable(self) -> "CompositeInstanceProtocol":
        """Lazy gateway to the atomic parameter instance."""
        ...

    @property
    def composite_class_immutable(self) -> "CompositeInstanceProtocol":
        """Lazy gateway to the atomic parameter instance."""
        ...