# class Convertible(IntMixin, FloatMixin, ComplexMixin, CeilMixin, FloorMixin, RoundMixin, TruncMixin):
#     """Podporuje int(), float(), round(), atd."""
#     __slots__ = ()

from .atoms import (
    IntMixin,
    FloatMixin,
    ComplexMixin,
    CeilMixin,
    FloorMixin,
    RoundMixin,
    TruncMixin,
)


class ConvertibleMixin(
    IntMixin,
    FloatMixin,
    ComplexMixin,
    CeilMixin,
    FloorMixin,
    RoundMixin,
    TruncMixin,
):
    """Podporuje int(), float(), round(), atd."""
    __slots__ = ()


IntFloatComplexCeilFloorRoundTruncMixin = ConvertibleMixin
