class BitwiseMixin(SimpleMixin):
    """
    Bitové operace pro SimpleObject atomy.
    Operace vrací novou instanci stejného typu se změněnou hodnotou.
    """

    __slots__ = ()

    # -------------------------
    # Helper: vytvoří novou instanci se stejným typem
    # -------------------------
    def _new_with_value(self, new_value):
        new = self.__class__()      # vytvoří instanci přes create_instance
        new.value = new_value       # aktivuje validaci + reaktivitu
        return new

    # -------------------------
    # &
    # -------------------------
    def __and__(self, other):
        other_value = getattr(other, "value", other)
        try:
            return self._new_with_value(self.value & other_value)
        except TypeError:
            return NotImplemented

    def __rand__(self, other):
        other_value = getattr(other, "value", other)
        try:
            return self._new_with_value(other_value & self.value)
        except TypeError:
            return NotImplemented

    # -------------------------
    # |
    # -------------------------
    def __or__(self, other):
        other_value = getattr(other, "value", other)
        try:
            return self._new_with_value(self.value | other_value)
        except TypeError:
            return NotImplemented

    def __ror__(self, other):
        other_value = getattr(other, "value", other)
        try:
            return self._new_with_value(other_value | self.value)
        except TypeError:
            return NotImplemented

    # -------------------------
    # ^
    # -------------------------
    def __xor__(self, other):
        other_value = getattr(other, "value", other)
        try:
            return self._new_with_value(self.value ^ other_value)
        except TypeError:
            return NotImplemented

    def __rxor__(self, other):
        other_value = getattr(other, "value", other)
        try:
            return self._new_with_value(other_value ^ self.value)
        except TypeError:
            return NotImplemented

    # -------------------------
    # <<
    # -------------------------
    def __lshift__(self, other):
        other_value = getattr(other, "value", other)
        try:
            return self._new_with_value(self.value << other_value)
        except TypeError:
            return NotImplemented

    def __rlshift__(self, other):
        other_value = getattr(other, "value", other)
        try:
            return self._new_with_value(other_value << self.value)
        except TypeError:
            return NotImplemented

    # -------------------------
    # >>
    # -------------------------
    def __rshift__(self, other):
        other_value = getattr(other, "value", other)
        try:
            return self._new_with_value(self.value >> other_value)
        except TypeError:
            return NotImplemented

    def __rrshift__(self, other):
        other_value = getattr(other, "value", other)
        try:
            return self._new_with_value(other_value >> self.value)
        except TypeError:
            return NotImplemented

    # -------------------------
    # ~x
    # -------------------------
    def __invert__(self):
        try:
            return self._new_with_value(~self.value)
        except TypeError:
            return NotImplemented
