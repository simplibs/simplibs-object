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
    Protokol pro mixin NodesDicts.

    Rozšiřuje NodesTuple o rychlé, neměnné vyhledávací slovníky (O(1) lookup),
    které mapují sub-node prvky podle jejich sémantických názvů (name_snake).
    """

    # --- TECHNICKÉ ATRIBUTY (Inicializované v init_mixins) ---

    # Mapuje name_snake na dvojici (živá_instance, její_relativní_cesta)
    _nodes_dict: NodesDict

    # Mapuje name_snake čistě na živou instanci sub-node prvku
    _nodes_instance_dict: "NodesInstanceDict"

    # Mapuje name_snake čistě na relativní cestu k prvku
    _nodes_path_dict: "NodesPathDict"

    # Mapuje name_snake na celočíselný index pozice uvnitř původního _nodes_tuple
    _nodes_index_map: "NodesIndexMap"