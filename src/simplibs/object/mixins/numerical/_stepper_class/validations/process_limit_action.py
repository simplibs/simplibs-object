from typing import Any, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .....protocols.mixins.numerical.stepper import StepperProtocol
    from .....protocols.mixins.numerical.stepper.internal_types import LimitAction


def process_limit_action(
    self: "StepperProtocol",
    value: Any
) -> "LimitAction":
    """
    Validuje a vrátí akci pro limit stepperu.

    Ověří, že zadaná hodnota je volatelný objekt (callable),
    který může být spuštěn při dosažení horního nebo spodního limitu.
    """

    # 1. Validace
    if not callable(value):
        raise ValueError("Akce musí být volatelný objekt")

    # 2. Navrácení hodnoty
    return value