from typing import Protocol, runtime_checkable, TYPE_CHECKING
# Inners
from .NodesTupleProtocol import NodesTupleProtocol
# Annotations
if TYPE_CHECKING:
    from ...alias_typings import (
        NodesDict,
        NodesInstanceDict,
        NodesPathDict,
        NodesIndexMap
    )


@runtime_checkable
class NodesDictsProtocol(
    NodesTupleProtocol,
    Protocol
):
    """
    Protocol for the NodesDicts mixin.

    Extends NodesTuple with fast, immutable lookup dictionaries (O(1) lookup)
    mapping sub-node elements by their semantic snake-case names (name_snake).
    """

    # --- TECHNICAL ATTRIBUTES (Initialized in init_mixins) ---

    # Maps name_snake to a tuple of (live_instance, relative_path)
    _nodes_dict: "NodesDict"

    # Maps name_snake strictly to the live instance of the sub-node element
    _nodes_instance_dict: "NodesInstanceDict"

    # Maps name_snake strictly to the relative path to the element
    _nodes_path_dict: "NodesPathDict"

    # Maps name_snake to the integer index position inside the original _nodes_tuple
    _nodes_index_map: "NodesIndexMap"