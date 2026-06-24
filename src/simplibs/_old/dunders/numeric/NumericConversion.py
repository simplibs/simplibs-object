import math
from numbers import Number
from ....base_class import SimpleMixin


class NumericConversionMixin(SimpleMixin):
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

    # -------------------------
    # int(x)
    # -------------------------
    def __int__(self) -> int:
        """Vrací nativní int(self.value)."""
        try:
            return int(self.value)
        except (TypeError, ValueError) as e:
            raise TypeError(
                f"Nelze převést {self.meta.class_name} (value={self.value!r}) na int: {e}"
            ) from e

    # -------------------------
    # float(x)
    # -------------------------
    def __float__(self) -> float:
        """Vrací nativní float(self.value)."""
        try:
            return float(self.value)
        except (TypeError, ValueError) as e:
            raise TypeError(
                f"Nelze převést {self.meta.class_name} (value={self.value!r}) na float: {e}"
            ) from e

    # -------------------------
    # complex(x)
    # -------------------------
    def __complex__(self) -> complex:
        """Vrací nativní complex(self.value)."""
        try:
            return complex(self.value)
        except (TypeError, ValueError) as e:
            raise TypeError(
                f"Nelze převést {self.meta.class_name} (value={self.value!r}) na complex: {e}"
            ) from e

    # -------------------------
    # index(x) — pro použití v slice, range, atd.
    # -------------------------
    def __index__(self) -> int:
        """
        Vrací nativní int(self.value) pro použití v range(), slice, atd.
        Musí vracet int, jinak vyhazuje TypeError.
        """
        value = self.value
        if not isinstance(value, int):
            raise TypeError(
                f"{self.meta.class_name} nelze použít jako index — "
                f"value musí být int, ne {type(value).__name__}."
            )
        return value

    # -------------------------
    # round(x, n)
    # -------------------------
    def __round__(self, n: int | None = None) -> int | float:
        """Vrací nativní round(self.value, n)."""
        try:
            return round(self.value, n)
        except (TypeError, ValueError) as e:
            raise TypeError(
                f"Nelze provést round() na {self.meta.class_name} (value={self.value!r}): {e}"
            ) from e

    # -------------------------
    # floor(x)
    # -------------------------
    def __floor__(self) -> int:
        """Vrací nativní math.floor(self.value)."""
        try:
            return math.floor(self.value)
        except (TypeError, ValueError) as e:
            raise TypeError(
                f"Nelze provést floor() na {self.meta.class_name} (value={self.value!r}): {e}"
            ) from e

    # -------------------------
    # ceil(x)
    # -------------------------
    def __ceil__(self) -> int:
        """Vrací nativní math.ceil(self.value)."""
        try:
            return math.ceil(self.value)
        except (TypeError, ValueError) as e:
            raise TypeError(
                f"Nelze provést ceil() na {self.meta.class_name} (value={self.value!r}): {e}"
            ) from e

    # -------------------------
    # trunc(x)
    # -------------------------
    def __trunc__(self) -> int:
        """Vrací nativní math.trunc(self.value)."""
        try:
            return math.trunc(self.value)
        except (TypeError, ValueError) as e:
            raise TypeError(
                f"Nelze provést trunc() na {self.meta.class_name} (value={self.value!r}): {e}"
            ) from e
