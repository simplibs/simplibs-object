# class Orderable(LtMixin, LeMixin, GtMixin, GeMixin):
#     """Podporuje <, <=, >, >="""
#     __slots__ = ()


from .atoms import LtMixin, LeMixin, GtMixin, GeMixin


class OrderableMixin(
    LtMixin,
    LeMixin,
    GtMixin,
    GeMixin,
):
    """Podporuje <, <=, >, >="""
    __slots__ = ()


LtLeGtGeMixin = OrderableMixin
