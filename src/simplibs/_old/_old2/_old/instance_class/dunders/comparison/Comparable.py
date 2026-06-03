# class Comparable(EqMixin, LtMixin, LeMixin, GtMixin, GeMixin):
#     """Podporuje ==, <, <=, >, >="""
#     __slots__ = ()

from .atoms import EqMixin, LtMixin, LeMixin, GtMixin, GeMixin


class ComparableMixin(
    EqMixin,
    LtMixin,
    LeMixin,
    GtMixin,
    GeMixin,
):
    """Podporuje ==, <, <=, >, >="""
    __slots__ = ()


EqLtLeGtGeMixin = ComparableMixin
