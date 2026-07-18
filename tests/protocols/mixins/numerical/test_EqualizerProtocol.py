from typing import Protocol, runtime_checkable, TYPE_CHECKING
# Outers
from ..core_mixins import NodesTupleProtocol
# Annotations
if TYPE_CHECKING:
    from .stepper import StepperProtocol
    from .internal_types import SteppersMap


@runtime_checkable
class EqualizerProtocol(
    NodesTupleProtocol,
    Protocol
):
    """
    Protokol pro mixin Equalizer.

    Garantuje přítomnost číselných ovladačů (stepperů) pro všechny sub-node prvky
    kompozice. Tyto ovladače jsou generovány dynamicky na základě blueprintu
    a jsou dostupné skrze dynamické properties s postfixem.
    """

    # --- TECHNICKÉ ATRIBUTY (Inicializované v init_mixins) ---

    # Mapuje vnitřní name_snake klíče prvků přímo na jejich příslušné instanční Steppery
    _steppers: "SteppersMap"

    # --- DYNAMICKÝ PŘÍSTUP K PROPERTIES ---

    def __getattr__(self, name: str) -> "StepperProtocol":
        """
        Dynamický fallback pro přístup k vygenerovaným vlastnostem stepperů jednotlivých uzlů
        (např. přístup k `obj.uzel_stepper`).

        Garantuje, že každý dynamicky vrácený ovladač splňuje rozhraní StepperProtocol.
        """
        ...