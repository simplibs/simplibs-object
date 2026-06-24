from types import MappingProxyType
# Outers
from ...base_class import SimpleMixin
# Inners
from ._utils.nodes import build_nodes_tuple


# noinspection PyAttributeOutsideInit
class Nodes(SimpleMixin):
    """
    Poskytuje serializaci instance do dict/JSON a obnovu z nich.
    Základ pro HistoryMixin.
    """

    __slots__ = (
        "_nodes_tuple",
        "_nodes_dict",
        "_nodes_instance_dict",
        "_nodes_path_dict",
        "_nodes_index_map"
    )

    def init_mixins(self):
        super().init_mixins()

        # Základní tuple s instancí a cestou, jako hlavní zdroj pravdy
        self._nodes_tuple = build_nodes_tuple(self)

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

    @property
    def nodes_tuple(self):
        """Základní tuple s instancí a cestou, jako hlavní zdroj pravdy"""
        return self._nodes_tuple

    @property
    def nodes_dict(self):
        """Základní neměnný slovník, pro přístup přes name_snake k nodes_tuple hodnotám"""
        return self._nodes_dict

    @property
    def nodes_instance_dict(self):
        """Neměný slovník obsahující přístup k instance přes name_snake"""
        return self._nodes_instance_dict

    @property
    def nodes_path_dict(self):
        """Neměný slovník obsahující přístup k cestě přes name_snake"""
        return self._nodes_path_dict

    @property
    def nodes_index_map(self):
        """Neměný slovník pro index pro přístup k položkám nodes_tuple"""
        return self._nodes_index_map