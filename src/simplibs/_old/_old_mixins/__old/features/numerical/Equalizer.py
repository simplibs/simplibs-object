# Outers
from ....protocols import SimpleInstanceType
from ..._validations import raise_mixin_cannot_by_add_to_constant
from ..._constants import STEPPER
from ..core_logic import NodesTuple
# Inners
from ._utils.stepper_class import Stepper



# noinspection PyAttributeOutsideInit
class Equalizer(NodesTuple):

    __slots__ = ("_steppers",)

    @staticmethod
    def __extend_instance_class__(instance_cls):

        # 1. Validace třídy (že není konstanta)
        if instance_cls.meta.is_constant:
            raise_mixin_cannot_by_add_to_constant("Equalizer", instance_cls)

        # 2. Vytvoření potřebných properties
        for name in instance_cls.meta.node_names_set:

            # 2.1 Definice getteru
            def getter(self, _name=name):
                return self._steppers[_name]

            # 2.2 Vytvoření property
            prop_name = f"{name}{STEPPER}"
            setattr(instance_cls, prop_name, property(getter))

        # 3. Navrácení pozměněné třídy
        return instance_cls

    def init_mixins(self: SimpleInstanceType):
        super().init_mixins()
        self._steppers = {
            instance.meta.name_snake: Stepper(instance)
            for instance, _ in self._nodes_tuple
        }
