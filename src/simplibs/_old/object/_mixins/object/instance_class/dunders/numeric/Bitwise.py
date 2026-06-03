# class Bitwise(AndMixin, OrMixin, XorMixin, InvertMixin, LshiftMixin, RshiftMixin):
#     """Podporuje &, |, ^, ~, <<, >>"""
#     __slots__ = ()

from .atoms import (
    AndMixin,
    OrMixin,
    XorMixin,
    InvertMixin,
    LshiftMixin,
    RshiftMixin,
)


class BitwiseMixin(
    AndMixin,
    OrMixin,
    XorMixin,
    InvertMixin,
    LshiftMixin,
    RshiftMixin,
):
    """Podporuje &, |, ^, ~, <<, >>"""
    __slots__ = ()


AndOrXorInvertLshiftRshiftMixin = BitwiseMixin
