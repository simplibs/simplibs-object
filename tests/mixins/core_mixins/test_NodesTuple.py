from typing import TYPE_CHECKING
# Outers
from ..base_class import SimpleMixin
from .._commons.constants import VALUE
# Inners
from ._utils.nodes_tuple import build_nodes_tuple
# Annotations
if TYPE_CHECKING:
    from ..._core.protocols.mixins.core_mixins import NodesTupleProtocol
    from ..._core.protocols.alias_typings import NamesTuple, NamesSet
    from ..._core.protocols.alias_typings import NodesTuple as _NodesTuple


class NodesTuple(SimpleMixin):
    """
    Poskytuje serializaci instance do dict/JSON a obnovu z nich.
    Základ pro HistoryMixin.
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice slotů
    __slots__ = (
        "_nodes_tuple",
        "_node_names_tuple"
        "_constant_names_tuple"
    )

    # ----------------------------------------
    # Hook pro inicializaci
    # ----------------------------------------

    # noinspection PyAttributeOutsideInit
    def init_mixins(
        self: "NodesTupleProtocol"
    ) -> None:

        # 1. Inicializace předků
        super().init_mixins()

        # 2. Základní tuple s instancí a cestou (hlavní zdroj pravdy)
        self._nodes_tuple: "_NodesTuple" = build_nodes_tuple(self)

        # 3. Tuple s jmény ve stejném pořadí jako _nodes_tuple
        self._node_names_tuple: "NamesTuple" = tuple(
            instance.meta.name_snake
            for instance, _ in self._nodes_tuple
        )

        # 4. Tuple s jmény konstant
        self._constant_names_tuple: "NamesSet" = {
            instance.meta.name_snake
            for instance, path in self._nodes_tuple
            if path[-1] is not VALUE
        }


