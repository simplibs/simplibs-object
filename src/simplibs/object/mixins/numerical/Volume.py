from numbers import Number
# Outers
from ....protocols import SimpleInstanceType
from ..base_class import SimpleMixin
# Innser
from ._utils.stepper_class import Stepper


# noinspection PyAttributeOutsideInit
class Volume(SimpleMixin):
    """
    Poskytuje přístup k stepperu pro hlavní hodnotu
    """

    # Definice určení
    _mutable_only = True
    _only_types = Number

    # Definice slotů
    __slots__ = ("_value_stepper",)

    # Inicializace mixinu
    def init_mixins(self: SimpleInstanceType):
        super().init_mixins()
        self._value_stepper = Stepper(self)

    @property
    def value_stepper(self):
        return self._value_stepper

