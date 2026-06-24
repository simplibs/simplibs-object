"""

Imutable mixin přepisuje value setter a vytváří novou instanci při každé změně a tu ttaké vrací.

Může možná využívat i Default Statte a možná i absorbovatkod z Permisions
"""
# Outers
from ...base_class import SimpleMixin
from ...._types import SimpleMetaType, SimpleInstanceType
# Inners
from ._utils.immutable import make_value_getter_only_on_class, make_all_inners_value_getter_only


# noinspection PyAttributeOutsideInit
class ImmutableMixin(SimpleMixin):
    """
    Mixin, který:
    - přepíše všechny .value property (root + všechny inners) na getter-only
    - tím znemožní jakoukoli přímou mutaci hodnoty setterem
    """

    __slots__ = ("_immutable_nodes",)

    @staticmethod
    def __extend_instance_class__(instance_cls):

        meta: SimpleMetaType = instance_cls.meta

        # 1) Přepsat .value na samotné instanční třídě
        make_value_getter_only_on_class(instance_cls)

        # 2) Rekurzivně projít celý strom inners a přepsat .value
        make_all_inners_value_getter_only(meta)

        # 3) (volitelné) – případně zde později přidáme with_value/with_inner API

        return instance_cls

    def init_mixins(self: SimpleInstanceType):
        super().init_mixins()
        self._immutable_nodes = {
            instance.meta.name_snake: instance
            for instance, _ in self._nodes_tuple
        }