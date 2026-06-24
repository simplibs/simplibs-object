from numbers import Number
from ....base_class import SimpleMixin


class NumericInplaceMixin(SimpleMixin):
    """
    Poskytuje in‑place aritmetické operace (+=, -=, *=, /=, //=, %=, **=)
    pro SimpleObject atomy a mutable instance.

    Operace:
    - mění hodnotu instance přes self.value = ...
    - aktivují validaci a reaktivitu
    - vrací self
    """

    __slots__ = ()

    # Pouze pro číselné typy
    _only_types = Number

    # Pouze pro mutable objekty
    _mutable_only = True

    # -------------------------
    # Helper
    # -------------------------
    @staticmethod
    def _extract_value(other):
        """Vrací other.value pokud existuje, jinak other."""
        return getattr(other, "value", other)

    # -------------------------
    # +=
    # -------------------------
    def __iadd__(self, other):
        """In‑place: self.value += other."""
        try:
            self.value = self.value + self._extract_value(other)
            return self
        except TypeError:
            return NotImplemented

    # -------------------------
    # -=
    # -------------------------
    def __isub__(self, other):
        """In‑place: self.value -= other."""
        try:
            self.value = self.value - self._extract_value(other)
            return self
        except TypeError:
            return NotImplemented

    # -------------------------
    # *=
    # -------------------------
    def __imul__(self, other):
        """In‑place: self.value *= other."""
        try:
            self.value = self.value * self._extract_value(other)
            return self
        except TypeError:
            return NotImplemented

    # -------------------------
    # /=
    # -------------------------
    def __itruediv__(self, other):
        """In‑place: self.value /= other."""
        try:
            self.value = self.value / self._extract_value(other)
            return self
        except (TypeError, ZeroDivisionError):
            return NotImplemented

    # -------------------------
    # //=
    # -------------------------
    def __ifloordiv__(self, other):
        """In‑place: self.value //= other."""
        try:
            self.value = self.value // self._extract_value(other)
            return self
        except (TypeError, ZeroDivisionError):
            return NotImplemented

    # -------------------------
    # %=
    # -------------------------
    def __imod__(self, other):
        """In‑place: self.value %= other."""
        try:
            self.value = self.value % self._extract_value(other)
            return self
        except (TypeError, ZeroDivisionError):
            return NotImplemented

    # -------------------------
    # **=
    # -------------------------
    def __ipow__(self, other):
        """In‑place: self.value **= other."""
        try:
            self.value = self.value ** self._extract_value(other)
            return self
        except TypeError:
            return NotImplemented
