# class Printable(ReprMixin, StrMixin, BoolMixin):
#     """Representable + __bool__"""
#     __slots__ = ()

from .atoms import ReprMixin, StrMixin, BoolMixin


class PrintableMixin(
    ReprMixin,
    StrMixin,
    BoolMixin,
):
    """Representable + __bool__"""
    __slots__ = ()


ReprStrBoolMixin = PrintableMixin
