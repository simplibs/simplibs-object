from numbers import Number
# Outers
from ....base_class import SimpleMixin
from ....imutable.state._utils.immutable_methods.with_composite import with_composite
from ...core_logic import NodesDicts, Snapshot
# Inners
from ._utils import coerce


class NumericArithmeticMixin(NodesDicts, Snapshot, SimpleMixin):
    """
    Poskytuje aritmetické operace (+, -, *, /, //, %, **) pro SimpleObject.

    Podporuje:
    - atomy (konstanty)
    - kompozice (přepočítává inners i owner hodnoty)

    Obsahuje lazy fallback konverzi typu:
    - pokud operace selže, pokusí se převést druhý operand na typ defaultní hodnoty
    - konverze se provádí pouze pokud je bezpečná (např. int → float/Decimal/Fraction)
    """

    __slots__ = ()

    # Omezení na číselné typy
    _only_types = Number

    # -------------------------
    # Helper
    # -------------------------
    def _apply(self, new_value):
        """
        Aplikuje novou hodnotu na instanci (atom nebo kompozici).
        Používá with_composite → přepočítá inners i owner hodnoty.
        """
        return with_composite(self, self.meta.name_snake, new_value)

    # -------------------------
    # +
    # -------------------------
    def __add__(self, other):
        """Vrací novou instanci s hodnotou self.value + other (s lazy fallback konverzí)."""
        other_value = getattr(other, "value", other)
        try:
            return self._apply(self.value + other_value)
        except TypeError:
            coerced = coerce(self, other_value)
            try:
                return self._apply(self.value + coerced)
            except TypeError:
                return NotImplemented

    def __radd__(self, other):
        """Vrací novou instanci s hodnotou other + self.value (s lazy fallback konverzí)."""
        other_value = getattr(other, "value", other)
        try:
            return self._apply(other_value + self.value)
        except TypeError:
            coerced = coerce(self, other_value)
            try:
                return self._apply(coerced + self.value)
            except TypeError:
                return NotImplemented

    # -------------------------
    # -
    # -------------------------
    def __sub__(self, other):
        """Vrací novou instanci s hodnotou self.value - other (s lazy fallback konverzí)."""
        other_value = getattr(other, "value", other)
        try:
            return self._apply(self.value - other_value)
        except TypeError:
            coerced = coerce(self, other_value)
            try:
                return self._apply(self.value - coerced)
            except TypeError:
                return NotImplemented

    def __rsub__(self, other):
        """Vrací novou instanci s hodnotou other - self.value (s lazy fallback konverzí)."""
        other_value = getattr(other, "value", other)
        try:
            return self._apply(other_value - self.value)
        except TypeError:
            coerced = coerce(self, other_value)
            try:
                return self._apply(coerced - self.value)
            except TypeError:
                return NotImplemented

    # -------------------------
    # *
    # -------------------------
    def __mul__(self, other):
        """Vrací novou instanci s hodnotou self.value * other (s lazy fallback konverzí)."""
        other_value = getattr(other, "value", other)
        try:
            return self._apply(self.value * other_value)
        except TypeError:
            coerced = coerce(self, other_value)
            try:
                return self._apply(self.value * coerced)
            except TypeError:
                return NotImplemented

    def __rmul__(self, other):
        """Vrací novou instanci s hodnotou other * self.value (s lazy fallback konverzí)."""
        other_value = getattr(other, "value", other)
        try:
            return self._apply(other_value * self.value)
        except TypeError:
            coerced = coerce(self, other_value)
            try:
                return self._apply(coerced * self.value)
            except TypeError:
                return NotImplemented

    # -------------------------
    # /
    # -------------------------
    def __truediv__(self, other):
        """Vrací novou instanci s hodnotou self.value / other (s lazy fallback konverzí)."""
        other_value = getattr(other, "value", other)
        try:
            return self._apply(self.value / other_value)
        except TypeError:
            coerced = coerce(self, other_value)
            try:
                return self._apply(self.value / coerced)
            except TypeError:
                return NotImplemented

    def __rtruediv__(self, other):
        """Vrací novou instanci s hodnotou other / self.value (s lazy fallback konverzí)."""
        other_value = getattr(other, "value", other)
        try:
            return self._apply(other_value / self.value)
        except TypeError:
            coerced = coerce(self, other_value)
            try:
                return self._apply(coerced / self.value)
            except TypeError:
                return NotImplemented

    # -------------------------
    # //
    # -------------------------
    def __floordiv__(self, other):
        """Vrací novou instanci s hodnotou self.value // other (s lazy fallback konverzí)."""
        other_value = getattr(other, "value", other)
        try:
            return self._apply(self.value // other_value)
        except TypeError:
            coerced = coerce(self, other_value)
            try:
                return self._apply(self.value // coerced)
            except TypeError:
                return NotImplemented

    def __rfloordiv__(self, other):
        """Vrací novou instanci s hodnotou other // self.value (s lazy fallback konverzí)."""
        other_value = getattr(other, "value", other)
        try:
            return self._apply(other_value // self.value)
        except TypeError:
            coerced = coerce(self, other_value)
            try:
                return self._apply(coerced // self.value)
            except TypeError:
                return NotImplemented

    # -------------------------
    # %
    # -------------------------
    def __mod__(self, other):
        """Vrací novou instanci s hodnotou self.value % other (s lazy fallback konverzí)."""
        other_value = getattr(other, "value", other)
        try:
            return self._apply(self.value % other_value)
        except TypeError:
            coerced = coerce(self, other_value)
            try:
                return self._apply(self.value % coerced)
            except TypeError:
                return NotImplemented

    def __rmod__(self, other):
        """Vrací novou instanci s hodnotou other % self.value (s lazy fallback konverzí)."""
        other_value = getattr(other, "value", other)
        try:
            return self._apply(other_value % self.value)
        except TypeError:
            coerced = coerce(self, other_value)
            try:
                return self._apply(coerced % self.value)
            except TypeError:
                return NotImplemented

    # -------------------------
    # **
    # -------------------------
    def __pow__(self, other):
        """Vrací novou instanci s hodnotou self.value ** other (s lazy fallback konverzí)."""
        other_value = getattr(other, "value", other)
        try:
            return self._apply(self.value ** other_value)
        except TypeError:
            coerced = coerce(self, other_value)
            try:
                return self._apply(self.value ** coerced)
            except TypeError:
                return NotImplemented

    def __rpow__(self, other):
        """Vrací novou instanci s hodnotou other ** self.value (s lazy fallback konverzí)."""
        other_value = getattr(other, "value", other)
        try:
            return self._apply(other_value ** self.value)
        except TypeError:
            coerced = coerce(self, other_value)
            try:
                return self._apply(coerced ** self.value)
            except TypeError:
                return NotImplemented
