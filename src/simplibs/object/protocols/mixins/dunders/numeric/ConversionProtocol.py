from typing import Protocol, runtime_checkable, Any
# Outers
from ...base_class import SimpleMixinProtocol


@runtime_checkable
class ConversionProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protokol pro mixin Conversion.

    Garantuje sadu standardních konverzních a matematických metod,
    které převádějí vnitřní hodnotu objektu na nativní Python typy.
    """

    # ---------------------------------------------------------
    # Základní typové konverze
    # ---------------------------------------------------------
    def __int__(self) -> int:
        """Vrací nativní int vyvozený z hodnoty objektu."""
        ...

    def __float__(self) -> float:
        """Vrací nativní float vyvozený z hodnoty objektu."""
        ...

    def __complex__(self) -> complex:
        """Vrací nativní complex vyvozený z hodnoty objektu."""
        ...

    def __index__(self) -> int:
        """
        Vrací čistý int pro použití objektu jako indexu (slice, range, atd.).
        Musí vracet striktní int, jinak Python vyvolá TypeError.
        """
        ...

    # ---------------------------------------------------------
    # Matematické ořezy a zaokrouhlování
    # ---------------------------------------------------------
    def __round__(self, n: int | None = None) -> int | float:
        """Vrací nativní zaokrouhlenou hodnotu na 'n' desetinných míst."""
        ...

    def __floor__(self) -> int:
        """Vrací nativní zaokrouhlené celé číslo dolů (math.floor)."""
        ...

    def __ceil__(self) -> int:
        """Vrací nativní zaokrouhlené celé číslo nahoru (math.ceil)."""
        ...

    def __trunc__(self) -> int:
        """Vrací nativní oříznuté celé číslo směrem k nule (math.trunc)."""
        ...