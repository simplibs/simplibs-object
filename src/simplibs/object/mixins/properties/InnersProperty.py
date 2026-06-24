# Outers
from ..base_class import SimpleMixin
# Inners
from ._utils.inners_property import collect_all_nested_properties


class InnersProperty(SimpleMixin):

    # Definice určení
    _composite_only = True

    # Definice slotů
    __slots__ = ()

    # ---------------------------------------------------------
    # 1) Hook volaný z create_instance
    # ---------------------------------------------------------

    @staticmethod
    def __extend_instance_class__(instance_cls):

        # 1. Vytvoření potřebných properties
        nested_props = collect_all_nested_properties(instance_cls.meta)

        # 2. Připojení atributů k třídě
        for name, prop in nested_props.items():
            setattr(instance_cls, name, prop)

        # 3. Navrácení pozměněné třídy
        return instance_cls