# class Representable(ReprMixin, StrMixin):
#     """Objekt má __repr__ a __str__"""
#     __slots__ = ()

from .atoms import ReprMixin, StrMixin


class RepresentableMixin(
    ReprMixin,
    StrMixin,
):
    """Objekt má __repr__ a __str__"""
    __slots__ = ()


ReprStrMixin = RepresentableMixin
