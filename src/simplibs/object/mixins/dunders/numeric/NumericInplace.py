class NumericInplaceMixin(SimpleMixin):
    """
    In‑place aritmetické operace pro SimpleObject atomy.
    Operace mění hodnotu instance a vrací self.
    """

    __slots__ = ()

    # -------------------------
    # Helper: získá hodnotu z other
    # -------------------------
    @staticmethod
    def _extract_value(other):
        return getattr(other, "value", other)

    # -------------------------
    # +=
    # -------------------------
    def __iadd__(self, other):
        try:
            self.value = self.value + self._extract_value(other)
            return self
        except TypeError:
            return NotImplemented

    # -------------------------
    # -=
    # -------------------------
    def __isub__(self, other):
        try:
            self.value = self.value - self._extract_value(other)
            return self
        except TypeError:
            return NotImplemented

    # -------------------------
    # *=
    # -------------------------
    def __imul__(self, other):
        try:
            self.value = self.value * self._extract_value(other)
            return self
        except TypeError:
            return NotImplemented

    # -------------------------
    # /=
    # -------------------------
    def __itruediv__(self, other):
        try:
            self.value = self.value / self._extract_value(other)
            return self
        except (TypeError, ZeroDivisionError):
            return NotImplemented

    # -------------------------
    # //=
    # -------------------------
    def __ifloordiv__(self, other):
        try:
            self.value = self.value // self._extract_value(other)
            return self
        except (TypeError, ZeroDivisionError):
            return NotImplemented

    # -------------------------
    # %=
    # -------------------------
    def __imod__(self, other):
        try:
            self.value = self.value % self._extract_value(other)
            return self
        except (TypeError, ZeroDivisionError):
            return NotImplemented

    # -------------------------
    # **=
    # -------------------------
    def __ipow__(self, other):
        try:
            self.value = self.value ** self._extract_value(other)
            return self
        except (TypeError, ZeroDivisionError):
            return NotImplemented
