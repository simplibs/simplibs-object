from typing import TYPE_CHECKING
from types import MappingProxyType
# Inners
from .NodesTuple import NodesTuple
# Annotations
if TYPE_CHECKING:
    from ...protocols.mixins.core_mixins import NodesDictsProtocol
    from ...protocols.alias_typings import NodesDict, NodesInstanceDict, NodesPathDict, NodesIndexMap


class NodesDicts(NodesTuple):
    """
    Poskytuje serializaci instance do dict/JSON a obnovu z nich.
    Základ pro HistoryMixin.
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice slotů
    __slots__ = (
        "_nodes_dict",
        "_nodes_instance_dict",
        "_nodes_path_dict",
        "_nodes_index_map"
    )

    # ----------------------------------------
    # Hook pro inicializaci
    # ----------------------------------------

    # noinspection PyAttributeOutsideInit
    def init_mixins(
        self: "NodesDictsProtocol"
    ) -> None:
        """
        Metoda, předávající svojí logiku do inicializačního procesu instance.
        """

        # 1. Inicializace předků
        super().init_mixins()

        # 2. Základní neměnný slovník, pro přístup přes name_snake k nodes_tuple hodnotám
        self._nodes_dict: "NodesDict" = MappingProxyType({
            instance.meta.name_snake: (instance, path)
            for instance, path in self._nodes_tuple
        })

        # 3. Neměný slovník obsahující přístup k instance přes name_snake
        self._nodes_instance_dict: "NodesInstanceDict" = MappingProxyType({
            instance.meta.name_snake: instance
            for instance, _ in self._nodes_tuple
        })

        # 4. Neměný slovník obsahující přístup k cestě přes name_snake
        self._nodes_path_dict: "NodesPathDict" = MappingProxyType({
            instance.meta.name_snake: path
            for instance, path in self._nodes_tuple
        })

        # 5. Neměný slovník pro index pro přístup k položkám nodes_tuple
        self._nodes_index_map: "NodesIndexMap" = MappingProxyType({
            instance.meta.name_snake: index
            for index, (instance, _) in enumerate(self._nodes_tuple)
        })

