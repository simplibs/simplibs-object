from typing import Protocol, runtime_checkable
# Outers
from ...common.core_logic import NodesTupleProtocol
# Inners
from .stepper import StepperProtocol


@runtime_checkable
class EqualizerProtocol(NodesTupleProtocol, Protocol):
    """
    Protokol pro mixin Equalizer.

    Garantuje přítomnost číselných ovladačů (stepperů) pro všechny sub-node prvky
    kompozice. Tyto ovladače jsou generovány dynamicky na základě blueprintu
    a jsou dostupné skrze dynamické properties s postfixem.
    """

    # --- TECHNICKÉ ATRIBUTY (Inicializované v init_mixins) ---

    # Mapuje vnitřní name_snake klíče prvků přímo na jejich příslušné instanční Steppery
    _steppers: dict[str, StepperProtocol]

    # --- DYNAMICKÝ PŘÍSTUP K PROPERTIES ---

    def __getattr__(self, name: str) -> StepperProtocol:
        """
        Dynamický fallback pro přístup k vygenerovaným vlastnostem stepperů jednotlivých uzlů
        (např. přístup k `obj.uzel_stepper`).

        Garantuje, že každý dynamicky vrácený ovladač splňuje rozhraní StepperProtocol.
        """
        ...