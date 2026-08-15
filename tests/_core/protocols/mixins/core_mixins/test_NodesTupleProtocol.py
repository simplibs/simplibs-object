from typing import Protocol, runtime_checkable, TYPE_CHECKING, TypeAlias
# Outers
from ..base_class import SimpleMixinProtocol
# Annotations
if TYPE_CHECKING:
    from ...alias_typings import NodesTuple, NamesTuple


@runtime_checkable
class NodesTupleProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protocol for the NodesTuple mixin.

    Guarantees the presence of tuples containing flattened sub-node instances,
    serving as the primary source of truth for serialization and history management.
    """

    # --- TECHNICAL ATTRIBUTES (Initialized in init_mixins) ---

    # Contains a tuple of pairs: (live_element_instance, relative_path)
    _nodes_tuple: "NodesTuple"

    # Contains a tuple of clean snake_case names for all sub-node elements
    _node_names_tuple: "NamesTuple"

    # Set of snake_case names for all internal constant (atomic) elements
    _constant_names_tuple: set[str]