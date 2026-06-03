# class Numeric(
#     AddMixin, SubMixin, MulMixin, DivMixin, FloordivMixin, ModMixin, PowMixin,
#     IntMixin, FloatMixin, AbsMixin, NegMixin, PosMixin
# ):
#     """Plné numerické chování"""
#     __slots__ = ()

from .atoms import (
    AddMixin,
    SubMixin,
    MulMixin,
    DivMixin,
    FloordivMixin,
    ModMixin,
    PowMixin,
    IntMixin,
    FloatMixin,
    AbsMixin,
    NegMixin,
    PosMixin,
)


class NumericMixin(
    AddMixin,
    SubMixin,
    MulMixin,
    DivMixin,
    FloordivMixin,
    ModMixin,
    PowMixin,
    IntMixin,
    FloatMixin,
    AbsMixin,
    NegMixin,
    PosMixin,
):
    """Plné numerické chování"""
    __slots__ = ()


AddSubMulDivFloordivModPowIntFloatAbsNegPosMixin = NumericMixin
