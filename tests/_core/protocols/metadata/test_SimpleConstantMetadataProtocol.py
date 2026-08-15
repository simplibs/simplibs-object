from typing import Protocol, Any, runtime_checkable, TYPE_CHECKING, Callable
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
    """
    Protocol for atomic/constant class metadata specifications.

    Compiles type definitions, default values, and custom validation methods.
    Provides lazy-loaded gateways (atom_class_mutable, atom_class_immutable)
    for synthesising atomic runtime instance classes on demand.
    """

    # 1. User-provided data
    value_type: "ValidTypes"
    default: Any
    validate: Callable

    # 2. Public interface
    value_type_name: str
    is_constant: bool

    # 3. Cache interface
    _atom_class_mutable: "AtomInstanceProtocol"
    _atom_class_immutable: "AtomInstanceProtocol"

    # 4. Cache for instance classes (defined as read-only properties)
    @property
    def atom_class_mutable(self) -> "AtomInstanceProtocol":
        """Lazy gateway to the core parameter instance."""
        ...

    @property
    def atom_class_immutable(self) -> "AtomInstanceProtocol":
        """Lazy gateway to the core parameter instance."""
        ...