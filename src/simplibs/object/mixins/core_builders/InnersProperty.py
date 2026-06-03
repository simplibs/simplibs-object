# Outers
from ..base_class import SimpleMixin
# Inners
from ._inners_property_helpers import collect_all_nested_properties


class InnersProperty(SimpleMixin):

    __slots__ = ()
    _composite_only = True

    # ---------------------------------------------------------
    # 1) Hook volaný z create_instance → doplní _default_state
    # ---------------------------------------------------------
    @staticmethod
    def __extend_instance_class__(instance_cls):

        # 1. Načtení meta
        meta = instance_cls.meta

        # 2. Vytvoření potřebných properties
        nested_props = collect_all_nested_properties(meta)

        # 3. Připojení atributů k třídě
        for name, prop in nested_props.items():
            setattr(instance_cls, name, prop)

        # 4. Navrácení pozměněné třídy
        return instance_cls