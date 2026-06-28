from typing import TypeAlias, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ..stepper import StepperProtocol


# Rychlá mapa pro vyhledání servisního ovladače (Stepperu) podle snake_case názvu poduzlu
SteppersMap: TypeAlias = dict[str, "StepperProtocol"]