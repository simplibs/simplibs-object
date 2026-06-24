from numbers import Integral
from ....base_class import SimpleMixin
from ....imutable.state._utils.immutable_methods.with_constant import with_constant
from ...core_logic import NodesDicts, Snapshot


class BitwiseMixin(NodesDicts, Snapshot, SimpleMixin):
    """
    Poskytuje bitové operace (&, |, ^, <<, >>, ~) pro SimpleObject atomy.

    Vlastnosti:
    - funguje pouze pro atomy (konstanty)
    - funguje pouze pro integrální typy (int, vlastní integer-like typy)
    - operace jsou čisté → vrací novou instanci
    """

    __slots__ = ()

    # Pouze pro integrální typy
    _only_types = Integral

    # Pouze pro konstanty (atomy)
    _constant_only = True

    # -------------------------
    # Helper
    # -------------------------
    def _new(self, new_value):
        """
        Vytvoří novou instanci se stejným typem a novou hodnotou.
        Používá with_constant → správně aktivuje validaci a reaktivitu.
        """
        return with_constant(self, self.meta.name_snake, new_value)

    # -------------------------
    # &
    # -------------------------
    def __and__(self, other):
        """Vrací novou instanci s hodnotou self.value & other."""
        other_value = getattr(other, "value", other)
        try:
            return self._new(self.value & other_value)
        except TypeError:
            return NotImplemented

    def __rand__(self, other):
        """Vrací novou instanci s hodnotou other & self.value."""
        other_value = getattr(other, "value", other)
        try:
            return self._new(other_value & self.value)
        except TypeError:
            return NotImplemented

    # -------------------------
    # |
    # -------------------------
    def __or__(self, other):
        """Vrací novou instanci s hodnotou self.value | other."""
        other_value = getattr(other, "value", other)
        try:
            return self._new(self.value | other_value)
        except TypeError:
            return NotImplemented

    def __ror__(self, other):
        """Vrací novou instanci s hodnotou other | self.value."""
        other_value = getattr(other, "value", other)
        try:
            return self._new(other_value | self.value)
        except TypeError:
            return NotImplemented

    # -------------------------
    # ^
    # -------------------------
    def __xor__(self, other):
        """Vrací novou instanci s hodnotou self.value ^ other."""
        other_value = getattr(other, "value", other)
        try:
            return self._new(self.value ^ other_value)
        except TypeError:
            return NotImplemented

    def __rxor__(self, other):
        """Vrací novou instanci s hodnotou other ^ self.value."""
        other_value = getattr(other, "value", other)
        try:
            return self._new(other_value ^ self.value)
        except TypeError:
            return NotImplemented

    # -------------------------
    # <<
    # -------------------------
    def __lshift__(self, other):
        """Vrací novou instanci s hodnotou self.value << other."""
        other_value = getattr(other, "value", other)
        try:
            return self._new(self.value << other_value)
        except TypeError:
            return NotImplemented

    def __rlshift__(self, other):
        """Vrací novou instanci s hodnotou other << self.value."""
        other_value = getattr(other, "value", other)
        try:
            return self._new(other_value << self.value)
        except TypeError:
            return NotImplemented

    # -------------------------
    # >>
    # -------------------------
    def __rshift__(self, other):
        """Vrací novou instanci s hodnotou self.value >> other."""
        other_value = getattr(other, "value", other)
        try:
            return self._new(self.value >> other_value)
        except TypeError:
            return NotImplemented

    def __rrshift__(self, other):
        """Vrací novou instanci s hodnotou other >> self.value."""
        other_value = getattr(other, "value", other)
        try:
            return self._new(other_value >> self.value)
        except TypeError:
            return NotImplemented

    # -------------------------
    # ~x
    # -------------------------
    def __invert__(self):
        """Vrací novou instanci s hodnotou ~self.value."""
        try:
            return self._new(~self.value)
        except TypeError:
            return NotImplemented
