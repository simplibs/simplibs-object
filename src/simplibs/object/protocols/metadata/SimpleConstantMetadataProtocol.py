from typing import Protocol, Any, runtime_checkable, TYPE_CHECKING
from collections.abc import Callable
# Inners
from .SimpleBaseMetadataProtocol import SimpleBaseMetadataProtocol
# Annotations
if TYPE_CHECKING:
    from ..instance.core_classes import AtomInstanceProtocol
    from ..alias_typings import ValidTypes


@runtime_checkable
class SimpleConstantMetadataProtocol(
    SimpleBaseMetadataProtocol,
    Protocol
):

    # 1. Data předaná uživatelem
    value_type: "ValidTypes"
    default: Any
    validate: Callable

    # 2. Veřejné rozhraní
    value_type_name: str
    is_constant: bool

    # 3. Chache rozhraní
    _atom_class_mutable: "AtomInstanceProtocol"
    _atom_class_immutable: "AtomInstanceProtocol"

    # 4. Cache pro instanční třídy (definováno jako read-only property)
    @property
    def atom_class_mutable(self) -> "AtomInstanceProtocol":
        """Lazy brána k core instanci parametru."""
        ...

    @property
    def atom_class_immutable(self) -> "AtomInstanceProtocol":
        """Lazy brána k core instanci parametru."""
        ...