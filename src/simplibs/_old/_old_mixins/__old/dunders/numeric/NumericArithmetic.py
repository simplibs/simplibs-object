class NumericArithmeticMixin(SimpleMixin):
    """
    Aritmetické operace pro Simple atomy.
    Každá operace vrací novou instanci stejného typu se změněnou hodnotou.
    Vytváření přes self.__class__() zajišťuje plný průchod validací a reaktivitou.
    """

    __slots__ = ()

    # -------------------------
    # Helper: vytvoří novou instanci se stejným typem
    # -------------------------
    def _new_with_value(self, new_value: Any) -> Any:
        """Vytvoří novou instanci stejného typu s danou hodnotou."""
        new = self.__class__()
        new.value = new_value
        return new

    # -------------------------
    # +
    # -------------------------
    def __add__(self, other: Any) -> Any:
        other_value = getattr(other, "value", other)
        try:
            return self._new_with_value(self.value + other_value)
        except TypeError:
            return NotImplemented

    def __radd__(self, other: Any) -> Any:
        return self.__add__(other)

    # -------------------------
    # -
    # -------------------------
    def __sub__(self, other: Any) -> Any:
        other_value = getattr(other, "value", other)
        try:
            return self._new_with_value(self.value - other_value)
        except TypeError:
            return NotImplemented

    def __rsub__(self, other: Any) -> Any:
        other_value = getattr(other, "value", other)
        try:
            return self._new_with_value(other_value - self.value)
        except TypeError:
            return NotImplemented

    # -------------------------
    # *
    # -------------------------
    def __mul__(self, other: Any) -> Any:
        other_value = getattr(other, "value", other)
        try:
            return self._new_with_value(self.value * other_value)
        except TypeError:
            return NotImplemented

    def __rmul__(self, other: Any) -> Any:
        return self.__mul__(other)

    # -------------------------
    # /
    # -------------------------
    def __truediv__(self, other: Any) -> Any:
        other_value = getattr(other, "value", other)
        try:
            return self._new_with_value(self.value / other_value)
        except (TypeError, ZeroDivisionError):
            return NotImplemented

    def __rtruediv__(self, other: Any) -> Any:
        other_value = getattr(other, "value", other)
        try:
            return self._new_with_value(other_value / self.value)
        except (TypeError, ZeroDivisionError):
            return NotImplemented

    # -------------------------
    # //
    # -------------------------
    def __floordiv__(self, other: Any) -> Any:
        other_value = getattr(other, "value", other)
        try:
            return self._new_with_value(self.value // other_value)
        except (TypeError, ZeroDivisionError):
            return NotImplemented

    def __rfloordiv__(self, other: Any) -> Any:
        other_value = getattr(other, "value", other)
        try:
            return self._new_with_value(other_value // self.value)
        except (TypeError, ZeroDivisionError):
            return NotImplemented

    # -------------------------
    # %
    # -------------------------
    def __mod__(self, other: Any) -> Any:
        other_value = getattr(other, "value", other)
        try:
            return self._new_with_value(self.value % other_value)
        except (TypeError, ZeroDivisionError):
            return NotImplemented

    def __rmod__(self, other: Any) -> Any:
        other_value = getattr(other, "value", other)
        try:
            return self._new_with_value(other_value % self.value)
        except (TypeError, ZeroDivisionError):
            return NotImplemented

    # -------------------------
    # **
    # -------------------------
    def __pow__(self, other: Any) -> Any:
        other_value = getattr(other, "value", other)
        try:
            return self._new_with_value(self.value ** other_value)
        except (TypeError, ZeroDivisionError):
            return NotImplemented

    def __rpow__(self, other: Any) -> Any:
        other_value = getattr(other, "value", other)
        try:
            return self._new_with_value(other_value ** self.value)
        except (TypeError, ZeroDivisionError):
            return NotImplemented