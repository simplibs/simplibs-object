# Outers
from ...base_class import SimpleMixin
from ....protocols import SimpleInstanceType
# Innser
from ._utils.stepper_class import Stepper


# noinspection PyAttributeOutsideInit
class Volume(SimpleMixin):
    """
    Poskytuje přístup k stepperu pro hlavní hodnotu
    """

    __slots__ = ("_value_stepper",)

    def init_mixins(self: SimpleInstanceType):
        super().init_mixins()
        self._value_stepper = Stepper(self)

    @property
    def value_stepper(self):
        return self._value_stepper

