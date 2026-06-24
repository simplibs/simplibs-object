import math
from numbers import Number
# Outers
from ...base_class import SimpleMixin
#Inners
from ._utils.conversion import execute_conv


class Conversion(SimpleMixin):
    """
    Poskytuje konverzní dundery (int, float, complex, index, round, floor, ceil, trunc)
    pro SimpleObject atomy i kompozice.

    Tyto metody:
    - vrací nativní Pythoní typy (int, float, complex, ...)
    - nevrací SimpleObject
    - vyhazují TypeError při nevalidní konverzi
    """

    __slots__ = ()

    # Omezení na číselné typy
    _only_types = Number

    # ---------------------------------------------------------
    # int(x), float(x), complex(x)
    # ---------------------------------------------------------
    def __int__(self) -> int:
        """Vrací nativní int(self.value)."""
        return execute_conv(self, int)

    def __float__(self) -> float:
        """Vrací nativní float(self.value)."""
        return execute_conv(self, float)

    def __complex__(self) -> complex:
        """Vrací nativní complex(self.value)."""
        return execute_conv(self, complex)

    # ---------------------------------------------------------
    # index(x) — pro použití v slice, range, atd.
    # ---------------------------------------------------------
    def __index__(self) -> int:
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

    # ---------------------------------------------------------
    # round(x, n)
    # ---------------------------------------------------------
    def __round__(self, n: int | None = None) -> int | float:
        """Vrací nativní round(self.value, n)."""
        return execute_conv(self, round, n) if n is not None else execute_conv(self, round)

    # ---------------------------------------------------------
    # floor(x), ceil(x), trunc(x)
    # ---------------------------------------------------------
    def __floor__(self) -> int:
        """Vrací nativní math.floor(self.value)."""
        return execute_conv(self, math.floor)

    def __ceil__(self) -> int:
        """Vrací nativní math.ceil(self.value)."""
        return execute_conv(self, math.ceil)

    def __trunc__(self) -> int:
        """Vrací nativní math.trunc(self.value)."""
        return execute_conv(self, math.trunc)