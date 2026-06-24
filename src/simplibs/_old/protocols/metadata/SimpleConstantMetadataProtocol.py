from typing import Protocol, Any, Callable, runtime_checkable, Union
# Inners
from .SimpleBaseMetadataProtocol import SimpleBaseMetadataProtocol


@runtime_checkable
class SimpleConstantMetadataProtocol(SimpleBaseMetadataProtocol, Protocol):

    # 1. Data předaná uživatelem
    value_type: type | Union
    default: Any
    validate: Callable

    # 2. Veřejné rozhraní
    value_type_name: str
    is_constant: bool

    # 3. Cache pro instanční třídy (definováno jako read-only property)
    @property
    def atom_class_mutable(self) -> type:
        """Lazy brána k core instanci parametru."""
        ...

    @property
    def atom_class_immutable(self) -> type:
        """Lazy brána k core instanci parametru."""
        ...