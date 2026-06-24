class NumericUnaryMixin(SimpleMixin):
    """
    Unární operace pro SimpleObject atomy.
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
    # -x
    # -------------------------
    def __neg__(self):
        try:
            return self._new_with_value(-self.value)
        except TypeError:
            return NotImplemented

    # -------------------------
    # +x
    # -------------------------
    def __pos__(self):
        try:
            return self._new_with_value(+self.value)
        except TypeError:
            return NotImplemented

    # -------------------------
    # abs(x)
    # -------------------------
    def __abs__(self):
        try:
            return self._new_with_value(abs(self.value))
        except TypeError:
            return NotImplemented
