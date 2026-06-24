from typing import Protocol, runtime_checkable
# Outers
from ....types import SimpleInstanceType


@runtime_checkable
class NodesTupleProtocol(SimpleInstanceType, Protocol):
    """
    Protokol pro mixin NodesTuple.

    Garantuje přítomnost n-tic (tuples) s rozloženými instancemi sub-node prvků,
    které slouží jako hlavní zdroj pravdy pro serializaci a správu historie.
    """

    # --- TECHNICKÉ ATRIBUTY (Inicializované v init_mixins) ---

    # Obsahuje n-tici dvojic (živá_instance_prvku, její_relativní_cesta)
    _nodes_tuple: tuple[tuple[SimpleInstanceType, str], ...]

    # Obsahuje n-tici čistých name_snake názvů všech sub-node prvků
    _node_names_tuple: tuple[str, ...]