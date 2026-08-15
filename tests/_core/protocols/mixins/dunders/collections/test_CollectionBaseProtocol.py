from typing import Protocol, runtime_checkable, TYPE_CHECKING
# outers
from ...base_class import SimpleMixinProtocol
# Annotations
if TYPE_CHECKING:
    from ...core_mixins.NodesTupleProtocol import NamesTuple
    from ....alias_typings import NamesSet, NamesTuple


@runtime_checkable
class CollectionBaseProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protocol for the CollectionBase mixin.

    Guarantees the core mapping API for composite instances (O(1) lookups
    and deterministic key ordering based on the blueprint).
    """

    # --- TECHNICAL ATTRIBUTES (Initialized in init_mixins) ---
    _inners_name_set: "NamesSet"
    _inners_name_tuple: "NamesTuple"

    # --- PUBLIC MAPPING API ---
    def keys(self) -> list[str]:
        """Returns a list of keys (name_snake) for all direct inner elements (inners)."""
        ...

    def values(self) -> list[object]:
        """Returns a list of values corresponding to individual inner elements (inners)."""
        ...

    def items(self) -> list[tuple[str, object]]:
        """Returns a list of (key, value) pairs for all inner elements (inners)."""
        ...