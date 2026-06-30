from typing import TYPE_CHECKING
import math
from numbers import Number
# Outers
from ...base_class import SimpleMixin
#Inners
from ._utils import execute_conversion
# Annotations
if TYPE_CHECKING:
    from ....protocols.mixins.dunders.numeric import ConversionProtocol


class Conversion(SimpleMixin):
    """
    Poskytuje konverzní dundery (int, float, complex, index, round, floor, ceil, trunc)
    pro SimpleObject atomy i kompozice.

    Tyto metody:
    - vrací nativní Pythoní typy (int, float, complex, ...)
    - nevrací SimpleObject
    - vyhazují TypeError při nevalidní konverzi
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice určení
    _only_types = Number

    # Definice slotů
    __slots__ = ()

    # ----------------------------------------
    # Methods - INT / FLOAT / COMPLEX
    # ----------------------------------------
    def __int__(
        self: "ConversionProtocol"
    ) -> int:
        """Vrací nativní int(self.value)."""
        return execute_conversion(self, int)

    def __float__(
        self: "ConversionProtocol"
    ) -> float:
        """Vrací nativní float(self.value)."""
        return execute_conversion(self, float)

    def __complex__(
        self: "ConversionProtocol"
    ) -> complex:
        """Vrací nativní complex(self.value)."""
        return execute_conversion(self, complex)

    # ----------------------------------------
    # Methods - INDEX (pro použití v slice, range, atd.)
    # ----------------------------------------
    def __index__(
        self: "ConversionProtocol"
    ) -> int:
        """
        Vrací nativní int(self.value) pro použití v range(), slice, atd.
        Musí vracet přesný int, jinak Python vyhazuje TypeError.
        """
        value = self.value
        if not isinstance(value, int):
            raise TypeError(
                f"{self.meta.class_name} nelze použít jako index — "
                f"value musí být int, ne {type(value).__name__}."
            )
        return value

    # ----------------------------------------
    # Methods - ROUND
    # ----------------------------------------
    def __round__(
        self: "ConversionProtocol",
        n: int | None = None
    ) -> int | float:
        """Vrací nativní round(self.value, n)."""
        return (
            execute_conversion(self, round, n)
            if n is not None
            else execute_conversion(self, round)
        )

    # ----------------------------------------
    # Methods - FLOOR / CEIL / TRUNC
    # ----------------------------------------
    def __floor__(
        self: "ConversionProtocol"
    ) -> int:
        """Vrací nativní math.floor(self.value)."""
        return execute_conversion(self, math.floor)

    def __ceil__(
        self: "ConversionProtocol"
    ) -> int:
        """Vrací nativní math.ceil(self.value)."""
        return execute_conversion(self, math.ceil)

    def __trunc__(
        self: "ConversionProtocol"
    ) -> int:
        """Vrací nativní math.trunc(self.value)."""
        return execute_conversion(self, math.trunc)