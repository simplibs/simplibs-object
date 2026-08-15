from typing import Protocol, runtime_checkable, Any
# Outers
from ..base_class import SimpleMixinProtocol


@runtime_checkable
class MetaShortcutsProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protocol for the MetaShortcuts mixin.

    Guarantees the presence of ergonomic shortcuts (properties) directly on the instance,
    providing fast access to frequently queried class metadata.
    """

    # --- OBJECT IDENTITY ---
    @property
    def name_snake(self) -> str:
        """Snake_case name of the object's class (e.g., 'my_data')."""
        ...

    # --- TYPE INFORMATION ---
    @property
    def value_type(self) -> type:
        """Original Python type of the value represented by the object."""
        ...

    @property
    def default(self) -> Any:
        """Default value of the object defined in its metadata."""
        ...

    # --- OBJECT STRUCTURE ---
    @property
    def is_atom(self) -> bool:
        """Returns True if the object represents an Atom (has no inner elements)."""
        ...

    @property
    def is_composite(self) -> bool:
        """Returns True if the object represents a Composite (consists of inner elements)."""
        ...

    @property
    def is_decomposeable(self) -> bool:
        """Returns True if the object supports decomposition logic for its main value."""
        ...