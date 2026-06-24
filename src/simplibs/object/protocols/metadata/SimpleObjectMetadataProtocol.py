from typing import Protocol, Callable, runtime_checkable, TYPE_CHECKING
# Inners
from .SimpleConstantMetadataProtocol import SimpleConstantMetadataProtocol
# Annotations
if TYPE_CHECKING:
    from ..classes import SimpleClassLike

@runtime_checkable
class SimpleObjectMetadataProtocol(
    SimpleConstantMetadataProtocol,
    Protocol
):

    # 1. Data předaná uživatelem
    inners: tuple["SimpleClassLike", ...]
    logic: Callable
    decompose: Callable

    # 2. Mapy pro inners prvky
    inners_params_name: tuple[str, ...]
    inners_map: dict[str, "SimpleClassLike"]

    # 3. Veřejné rozhraní
    is_decomposeable: bool

    # 4. Cache pro instanční třídy (definováno jako read-only property)
    @property
    def composite_class_mutable(self) -> type:
        """Lazy brána k atomické instanci parametru."""
        ...

    @property
    def composite_class_immutable(self) -> type:
        """Lazy brána k atomické instanci parametru."""
        ...
