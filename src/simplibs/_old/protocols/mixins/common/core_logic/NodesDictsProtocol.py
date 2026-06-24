from typing import Protocol, runtime_checkable, Mapping
# Outers
from ....types import SimpleInstanceType
# Inners
from .NodesTupleProtocol import NodesTupleProtocol


@runtime_checkable
class NodesDictsProtocol(NodesTupleProtocol, Protocol):
    """
    Protokol pro mixin NodesDicts.

    Rozšiřuje NodesTuple o rychlé, neměnné vyhledávací slovníky (O(1) lookup),
    které mapují sub-node prvky podle jejich sémantických názvů (name_snake).
    """

    # --- TECHNICKÉ ATRIBUTY (Inicializované v init_mixins) ---

    # Mapuje name_snake na dvojici (živá_instance, její_relativní_cesta)
    _nodes_dict: Mapping[str, tuple[SimpleInstanceType, str]]

    # Mapuje name_snake čistě na živou instanci sub-node prvku
    _nodes_instance_dict: Mapping[str, SimpleInstanceType]

    # Mapuje name_snake čistě na relativní cestu k prvku
    _nodes_path_dict: Mapping[str, str]

    # Mapuje name_snake na celočíselný index pozice uvnitř původního _nodes_tuple
    _nodes_index_map: Mapping[str, int]