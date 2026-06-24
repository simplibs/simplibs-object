from typing import Any
# Outers
from ....protocols import SimpleInstanceType
from ..._constants import VALUE
from ..core_logic import Snapshot
# Inners
from ._utils.immutable.class_changers import make_all_inners_value_getter_only, make_value_getter_only_on_class
from ._utils.immutable.methods import with_constants, with_constant, with_composite


# noinspection PyProtectedMember
# noinspection PyAttributeOutsideInit
class ImmutableBase(Snapshot):
    """
    Mixin, který:
    - přepíše všechny .value property (root + všechny inners) na getter-only
    - tím znemožní jakoukoli přímou mutaci hodnoty setterem
    """

    __slots__ = ("_nodes_dict", "_constant_names")

    @staticmethod
    def __extend_instance_class__(instance_cls):

        # 1. Přepsat .value na samotné instanční třídě
        make_value_getter_only_on_class(instance_cls)

        # 2. Rekurzivně projít celý strom inners a přepsat .value
        make_all_inners_value_getter_only(instance_cls.meta)

        # 3. Navrácení upravené třídy
        return instance_cls

    def init_mixins(self):
        super().init_mixins()
        self._nodes_dict = {
            instance.meta.name_snake: (instance, path)
            for instance, path in self._nodes_tuple
        }
        self._constant_names = tuple(
            instance.meta.name_snake
            for instance, path in self._nodes_tuple
            if path[-1] is not VALUE
        )

    def _with_constants(
        self: SimpleInstanceType,
        changes: tuple[str, Any] | tuple[tuple[str, Any], ...] | None = None
    ) -> SimpleInstanceType:
        """Vytvoří instanci na základě předaných konstant"""
        return with_constants(self, changes)

    def _with_constant(
        self: SimpleInstanceType,
        name: str,
        new_value: Any
    ) -> SimpleInstanceType:
        """Vytvoří instanci na základě jména a nové hodnoty pro konstantu"""
        return with_constant(self, name, new_value)

    def _with_composite(
        self: SimpleInstanceType,
        name: str,
        new_value: Any
    ) -> SimpleInstanceType:
        """Vytvoří instanci na základě jména a nové hodnoty pro kompozici"""
        return with_composite(self, name, new_value)

