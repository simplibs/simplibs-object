class OrderingMixin(SimpleMixin):
    """
    Porovnávání velikosti pro Simple instance.
    Porovnává podle hodnoty (self.value).
    Funguje pro porovnání instance s instancí i s přímou hodnotou.
    """

    __slots__ = ()

    def __lt__(self, other: Any) -> bool:
        other_value = getattr(other, "value", other)
        try:
            return self.value < other_value
        except TypeError:
            return NotImplemented

    def __le__(self, other: Any) -> bool:
        other_value = getattr(other, "value", other)
        try:
            return self.value <= other_value
        except TypeError:
            return NotImplemented

    def __gt__(self, other: Any) -> bool:
        other_value = getattr(other, "value", other)
        try:
            return self.value > other_value
        except TypeError:
            return NotImplemented

    def __ge__(self, other: Any) -> bool:
        other_value = getattr(other, "value", other)
        try:
            return self.value >= other_value
        except TypeError:
            return NotImplemented