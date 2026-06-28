from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Outers
from ...validations import process_value
# Annotations
if TYPE_CHECKING:
    from ......protocols.mixins.numerical.stepper import StepperProtocol


def process_step_value(
    self: "StepperProtocol",
    value: Any = UNSET,
    *,
    validate: bool = True
) -> Any:
    """
    Připraví a normalizuje hodnotu kroku pro použití v metodách step_up a step_down.

    Pokud není hodnota zadána (UNSET), vrátí výchozí krok stepperu.
    Pokud je hodnota zadána, projde standardní normalizací a volitelnou validací.
    """
    return (
        self._step if value is UNSET
        else process_value(self, value, validate=validate)
    )