from typing import Protocol, runtime_checkable
# Outers
from ....types import SimpleInstanceType
# Inners
from .stepper import StepperProtocol


@runtime_checkable
class VolumeProtocol(SimpleInstanceType, Protocol):
    """
    Protokol pro mixin Volume.

    Garantuje přítomnost číselného ovladače (stepperu) přímo navázaného
    na hlavní hodnotu instance, což umožňuje bezpečné krokování a hlídání limitů.
    """

    # --- TECHNICKÉ ATRIBUTY (Inicializované v init_mixins) ---
    _value_stepper: StepperProtocol

    # --- VEŘEJNÉ API / PROPERTIES ---

    @property
    def value_stepper(self) -> StepperProtocol:
        """
        Vrací číselný ovladač (stepper) pro bezpečnou manipulaci
        s hlavní hodnotou této instance.
        """
        ...