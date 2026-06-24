from numbers import Number, Integral
# Outers
from ....base_class import SimpleMixin
from ....imutable.state._utils.immutable_methods.with_composite import with_composite
from ...core_logic import NodesDicts, Snapshot
# Inners
from ._utils import coerce


class NumericUnaryMixin(NodesDicts, Snapshot, SimpleMixin):
    """
    Poskytuje unární numerické operace (-x, +x, abs(x)) pro SimpleObject.

    Podporuje:
    - atomy (konstanty)
    - kompozice (přepočítává inners i owner hodnoty)

    Obsahuje lazy fallback konverzi typu:
    - pokud operace selže, pokusí se převést hodnotu na typ defaultní hodnoty
    - konverze se provádí pouze pokud je bezpečná (např. int → float/Decimal/Fraction)
    """

    __slots__ = ()

    # Omezení na číselné typy
    _only_types = Number

    # -------------------------
    # Helper: apply
    # -------------------------
    def _apply(self, new_value):
        """
        Aplikuje novou hodnotu na instanci (atom nebo kompozici).
        Používá with_composite → přepočítá inners i owner hodnoty.
        """
        return with_composite(self, self.meta.name_snake, new_value)

    # -------------------------
    # -x
    # -------------------------
    def __neg__(self):
        """Vrací novou instanci s hodnotou -self.value (s lazy fallback konverzí)."""
        try:
            return self._apply(-self.value)
        except TypeError:
            coerced = coerce(self, self.value)
            try:
                return self._apply(-coerced)
            except TypeError:
                return NotImplemented

    # -------------------------
    # +x
    # -------------------------
    def __pos__(self):
        """Vrací novou instanci s hodnotou +self.value (s lazy fallback konverzí)."""
        try:
            return self._apply(+self.value)
        except TypeError:
            coerced = coerce(self, self.value)
            try:
                return self._apply(+coerced)
            except TypeError:
                return NotImplemented

    # -------------------------
    # abs(x)
    # -------------------------
    def __abs__(self):
        """Vrací novou instanci s hodnotou abs(self.value) (s lazy fallback konverzí)."""
        try:
            return self._apply(abs(self.value))
        except TypeError:
            coerced = coerce(self, self.value)
            try:
                return self._apply(abs(coerced))
            except TypeError:
                return NotImplemented
