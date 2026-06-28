from typing import Protocol, runtime_checkable, TYPE_CHECKING
from collections.abc import Callable
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

    # 1. Data předaná uživatelem
    inners: "InnersTuple"
    logic: Callable
    decompose: Callable

    # 2. Mapy pro inners prvky
    inners_params_name: "NamesTuple"
    inners_map: "InnersMap"

    # 3. Veřejné rozhraní
    is_decomposeable: bool

    # 4. Chache rozhraní
    _composite_class_mutable: "CompositeInstanceProtocol"
    _composite_class_immutable: "CompositeInstanceProtocol"

    # 5. Cache pro instanční třídy (definováno jako read-only property)
    @property
    def composite_class_mutable(self) -> "CompositeInstanceProtocol":
        """Lazy brána k atomické instanci parametru."""
        ...

    @property
    def composite_class_immutable(self) -> "CompositeInstanceProtocol":
        """Lazy brána k atomické instanci parametru."""
        ...