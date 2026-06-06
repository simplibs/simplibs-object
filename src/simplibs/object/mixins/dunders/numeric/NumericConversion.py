import math

class NumericConversionMixin(SimpleMixin):
    """
    Konverzní dundery pro SimpleObject atomy.
    Vrací nativní Pythoní typy (int, float, complex, ...).
    """

    __slots__ = ()

    # -------------------------
    # int(x)
    # -------------------------
    def __int__(self) -> int:
        try:
            return int(self.value)
        except (TypeError, ValueError) as e:
            raise TypeError(
                f"Nelze převést {self.meta.class_name} "
                f"(value={self.value!r}) na int: {e}"
            ) from e

    # -------------------------
    # float(x)
    # -------------------------
    def __float__(self) -> float:
        try:
            return float(self.value)
        except (TypeError, ValueError) as e:
            raise TypeError(
                f"Nelze převést {self.meta.class_name} "
                f"(value={self.value!r}) na float: {e}"
            ) from e

    # -------------------------
    # complex(x)
    # -------------------------
    def __complex__(self) -> complex:
        try:
            return complex(self.value)
        except (TypeError, ValueError) as e:
            raise TypeError(
                f"Nelze převést {self.meta.class_name} "
                f"(value={self.value!r}) na complex: {e}"
            ) from e

    # -------------------------
    # index(x) — pro použití v slice, range, atd.
    # -------------------------
    def __index__(self) -> int:
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
        try:
            return round(self.value, n)
        except (TypeError, ValueError) as e:
            raise TypeError(
                f"Nelze provést round() na {self.meta.class_name} "
                f"(value={self.value!r}): {e}"
            ) from e

    # -------------------------
    # floor(x)
    # -------------------------
    def __floor__(self) -> int:
        try:
            return math.floor(self.value)
        except (TypeError, ValueError) as e:
            raise TypeError(
                f"Nelze provést floor() na {self.meta.class_name} "
                f"(value={self.value!r}): {e}"
            ) from e

    # -------------------------
    # ceil(x)
    # -------------------------
    def __ceil__(self) -> int:
        try:
            return math.ceil(self.value)
        except (TypeError, ValueError) as e:
            raise TypeError(
                f"Nelze provést ceil() na {self.meta.class_name} "
                f"(value={self.value!r}): {e}"
            ) from e

    # -------------------------
    # trunc(x)
    # -------------------------
    def __trunc__(self) -> int:
        try:
            return math.trunc(self.value)
        except (TypeError, ValueError) as e:
            raise TypeError(
                f"Nelze provést trunc() na {self.meta.class_name} "
                f"(value={self.value!r}): {e}"
            ) from e
