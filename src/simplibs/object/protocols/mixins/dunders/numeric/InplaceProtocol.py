from typing import Protocol, runtime_checkable, Any, Self
# Outers
from ...base_class import SimpleMixinProtocol


@runtime_checkable
class InplaceProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protokol pro mixin Inplace.

    Garantuje sadu in-place aritmetických operátorů (+=, -=, *=, /=, //=, %=, **=).
    Všechny operace modifikují hodnotu objektu na místě, spouštějí reaktivitu
    a vracejí upravenou instanci (Self).
    """

    # ---------------------------------------------------------
    # In-place sčítání (+=)
    # ---------------------------------------------------------
    def __iadd__(self, other: Any) -> Self:
        """Modifikuje hodnotu na místě: (self.value += other) a vrací self."""
        ...

    # ---------------------------------------------------------
    # In-place odčítání (-=)
    # ---------------------------------------------------------
    def __isub__(self, other: Any) -> Self:
        """Modifikuje hodnotu na místě: (self.value -= other) a vrací self."""
        ...

    # ---------------------------------------------------------
    # In-place násobení (*=)
    # ---------------------------------------------------------
    def __imul__(self, other: Any) -> Self:
        """Modifikuje hodnotu na místě: (self.value *= other) a vrací self."""
        ...

    # ---------------------------------------------------------
    # In-place dělení (/=)
    # ---------------------------------------------------------
    def __itruediv__(self, other: Any) -> Self:
        """Modifikuje hodnotu na místě: (self.value /= other) a vrací self."""
        ...

    # ---------------------------------------------------------
    # In-place celočíselné dělení (//=)
    # ---------------------------------------------------------
    def __ifloordiv__(self, other: Any) -> Self:
        """Modifikuje hodnotu na místě: (self.value //= other) a vrací self."""
        ...

    # ---------------------------------------------------------
    # In-place modulo (%=)
    # ---------------------------------------------------------
    def __imod__(self, other: Any) -> Self:
        """Modifikuje hodnotu na místě: (self.value %= other) a vrací self."""
        ...

    # ---------------------------------------------------------
    # In-place mocnina (**=)
    # ---------------------------------------------------------
    def __ipow__(self, other: Any) -> Self:
        """Modifikuje hodnotu na místě: (self.value **= other) a vrací self."""
        ...