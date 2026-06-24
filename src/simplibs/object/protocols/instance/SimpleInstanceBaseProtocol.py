from typing import Protocol, runtime_checkable


@runtime_checkable
class SimpleInstanceBaseProtocol(
    Protocol
):
    """
    Kořenový protokol pro všechny runtime instance v systému Simple.

    Může být založen na ConstantInstanceProtocol když je stavěn jako konstanta
    a nebo na CompositeInstanceProtocol když je stavěn
    (Zde je použit větší prvek pro pokrytí všech variant.)

    Zastřešuje společné technické dundery vštěpované tovární funkcí `create_instance`
    a garantuje přítomnost základního instančního rozhraní.
    """

    # --- TECHNICKÉ ATRIBUTY (Vštěpované továrnou create_instance) ---
    __is_constant__: bool
    __is_mutable__: bool
    __mixins__: tuple[type, ...]

