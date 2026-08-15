from typing import TYPE_CHECKING
from numbers import Number
# Outers
from ..base_class import SimpleMixin
# Innser
from ._stepper_class import Stepper
# Annotations
if TYPE_CHECKING:
    from ..._core.protocols.mixins.numerical import VolumeProtocol
    from ..._core.protocols.mixins.numerical.stepper import StepperProtocol


class Volume(SimpleMixin):
    """
    Poskytuje přístup k stepperu pro hlavní hodnotu.

    Garantuje přítomnost číselného ovladače (stepperu) přímo navázaného
    na hlavní hodnotu instance, což umožňuje bezpečné krokování a hlídání limitů.
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice určení
    _mutable_only = True
    _only_types = Number

    # Definice slotů
    __slots__ = ("_value_stepper",)

    # ----------------------------------------
    # Hook pro inicializaci
    # ----------------------------------------

    # noinspection PyAttributeOutsideInit
    def init_mixins(
        self: "VolumeProtocol"
    ) -> None:
        """
        Metoda, předávající svojí logiku do inicializačního procesu instance.
        """

        # 1. Inicializace předků
        super().init_mixins()

        # 2. Stepper pro základní hodnotu
        self._value_stepper: "StepperProtocol" = Stepper(self)

    # ----------------------------------------
    # Property - getters
    # ----------------------------------------

    @property
    def value_stepper(
        self: "VolumeProtocol"
    ) -> "StepperProtocol":
        """
        Vrací číselný ovladač (stepper) pro bezpečnou manipulaci
        s hlavní hodnotou této instance.
        """
        return self._value_stepper

