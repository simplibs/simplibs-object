from typing import Any, TYPE_CHECKING
# Inners
from .process_value import process_value
# Annotations
if TYPE_CHECKING:
    from .....protocols.mixins.numerical.stepper import StepperProtocol


def process_up_limit_value(
    self: "StepperProtocol",
    value: Any
) -> Any:
    """
    Připraví a validuje hodnotu horního limitu stepperu.

    Normalizuje zadanou hodnotu na správný typ a ověří,
    že horní limit není nižší než aktuálně nastavený spodní limit.
    """

    # 1. Příprava hodnoty
    _value = process_value(self, value)

    # 2. Validace
    if self.down_limit > _value:
        raise ValueError("Up limit nemůže být menší než down limit")

    return _value