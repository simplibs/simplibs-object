# Outers
from ..base_class import SimpleMixin
# Inners
from ._utils.nodes_tuple import build_nodes_tuple


# noinspection PyAttributeOutsideInit
class NodesTuple(SimpleMixin):
    """
    Poskytuje serializaci instance do dict/JSON a obnovu z nich.
    Základ pro HistoryMixin.
    """

    __slots__ = (
        "_nodes_tuple",
        "_node_names_tuple"
    )

    def init_mixins(self):
        super().init_mixins()

        # Základní tuple s instancí a cestou, jako hlavní zdroj pravdy
        self._nodes_tuple = build_nodes_tuple(self)
        self._node_names_tuple = tuple(instance.meta.name_snake for instance, _ in self._nodes_tuple)


