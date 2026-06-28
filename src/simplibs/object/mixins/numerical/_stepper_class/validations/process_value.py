from typing import Any, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .....protocols.mixins.numerical.stepper import StepperProtocol


def process_value(
    self: "StepperProtocol",
    value: Any,
    *,
    validate: bool = True
) -> Any:
    """
    Normalizuje a volitelně validuje hodnotu pro použití ve stepperu.

    Převede zadanou hodnotu na správný typ instance a volitelně
    ji ověří přes validační logiku navázané instance.
    """

    # 1. Normalizace hodnoty
    _value = (
        value if isinstance(value, self._value_type)
        else self._value_type(value)
    )

    # 2. Validace hodnoty
    if validate:
        self._instance.validate(_value)

    # 3. Navrácení hodnoty
    return _value