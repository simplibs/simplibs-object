from typing import TypeAlias, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ..stepper import StepperProtocol


# Fast mapping for retrieving a service controller (Stepper) by subnode snake_case name
SteppersMap: TypeAlias = dict[str, "StepperProtocol"]