from typing import Protocol, runtime_checkable, TYPE_CHECKING
# Outers
from ..base_class import SimpleMixinProtocol
# Annotations
if TYPE_CHECKING:
    from .stepper import StepperProtocol


@runtime_checkable
class VolumeProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protokol pro mixin Volume.

    Garantuje přítomnost číselného ovladače (stepperu) přímo navázaného
    na hlavní hodnotu instance, což umožňuje bezpečné krokování a hlídání limitů.
    """

    # --- TECHNICKÉ ATRIBUTY (Inicializované v init_mixins) ---
    _value_stepper: "StepperProtocol"

    # --- VEŘEJNÉ API / PROPERTIES ---

    @property
    def value_stepper(self) -> "StepperProtocol":
        """
        Vrací číselný ovladač (stepper) pro bezpečnou manipulaci
        s hlavní hodnotou této instance.
        """
        ...