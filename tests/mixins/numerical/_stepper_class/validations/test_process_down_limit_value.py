from typing import Any, TYPE_CHECKING
# Inners
from .process_value import process_value
# Annotations
if TYPE_CHECKING:
    from .....protocols.mixins.numerical.stepper import StepperProtocol


def process_down_limit_value(
    self: "StepperProtocol",
    value: Any
) -> Any:
    """
    Připraví a validuje hodnotu spodního limitu stepperu.

    Normalizuje zadanou hodnotu na správný typ a ověří,
    že spodní limit není vyšší než aktuálně nastavený horní limit.
    """

    # 1. Příprava hodnoty
    _value = process_value(self, value)

    # 2. Validace
    if self.up_limit < _value:
        raise ValueError("Down limit nemůže být vyšší než up limit")

    return _value