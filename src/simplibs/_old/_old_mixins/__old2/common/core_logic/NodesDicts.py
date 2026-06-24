from types import MappingProxyType
# Inners
from .NodesTuple import NodesTuple


# noinspection PyAttributeOutsideInit
class NodesDicts(NodesTuple):
    """
    Poskytuje serializaci instance do dict/JSON a obnovu z nich.
    Základ pro HistoryMixin.
    """

    __slots__ = (
        "_nodes_dict",
        "_nodes_instance_dict",
        "_nodes_path_dict",
        "_nodes_index_map"
    )

    def init_mixins(self):
        super().init_mixins()

        # Základní neměnný slovník, pro přístup přes name_snake k nodes_tuple hodnotám
        self._nodes_dict = MappingProxyType({
            instance.meta.name_snake: (instance, path)
            for instance, path in self._nodes_tuple
        })

        # Neměný slovník obsahující přístup k instance přes name_snake
        self._nodes_instance_dict = MappingProxyType({
            instance.meta.name_snake: instance
            for instance, _ in self._nodes_tuple
        })

        # Neměný slovník obsahující přístup k cestě přes name_snake
        self._nodes_path_dict = MappingProxyType({
            instance.meta.name_snake: path
            for instance, path in self._nodes_tuple
        })

        # Neměný slovník pro index pro přístup k položkám nodes_tuple
        self._nodes_index_map = MappingProxyType({
            instance.meta.name_snake: index
            for index, (instance, _) in enumerate(self._nodes_tuple)
        })

