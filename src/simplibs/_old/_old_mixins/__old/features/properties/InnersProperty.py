# Outers
from ...base_class import SimpleMixin
from ..._validations import raise_mixin_cannot_by_add_to_constant
# Inners
from ._utils.inners_property import collect_all_nested_properties


class InnersProperty(SimpleMixin):

    __slots__ = ()
    _composite_only = True

    # ---------------------------------------------------------
    # 1) Hook volaný z create_instance
    # ---------------------------------------------------------
    @staticmethod
    def __extend_instance_class__(instance_cls):

        # 1. Validace třídy (že není konstanta)
        if instance_cls.meta.is_constant:
            raise_mixin_cannot_by_add_to_constant("InnersProperty", instance_cls)

        # 2. Vytvoření potřebných properties
        nested_props = collect_all_nested_properties(instance_cls.meta)

        # 3. Připojení atributů k třídě
        for name, prop in nested_props.items():
            setattr(instance_cls, name, prop)

        # 4. Navrácení pozměněné třídy
        return instance_cls