# class Integer(
#     # arithmetic
#     AddMixin, SubMixin, MulMixin, DivMixin, FloordivMixin, ModMixin, PowMixin,
#     # bitwise
#     AndMixin, OrMixin, XorMixin, InvertMixin, LshiftMixin, RshiftMixin,
#     # conversions
#     IntMixin, IndexMixin,
#     # unary
#     AbsMixin, NegMixin, PosMixin
# ):
#     """Celé číslo — aritmetika + bitwise"""
#     __slots__ = ()

from .atoms import (
    # arithmetic
    AddMixin,
    SubMixin,
    MulMixin,
    DivMixin,
    FloordivMixin,
    ModMixin,
    PowMixin,
    # bitwise
    AndMixin,
    OrMixin,
    XorMixin,
    InvertMixin,
    LshiftMixin,
    RshiftMixin,
    # conversions
    IntMixin,
    IndexMixin,
    # unary
    AbsMixin,
    NegMixin,
    PosMixin,
)


class IntegerMixin(
    # arithmetic
    AddMixin,
    SubMixin,
    MulMixin,
    DivMixin,
    FloordivMixin,
    ModMixin,
    PowMixin,
    # bitwise
    AndMixin,
    OrMixin,
    XorMixin,
    InvertMixin,
    LshiftMixin,
    RshiftMixin,
    # conversions
    IntMixin,
    IndexMixin,
    # unary
    AbsMixin,
    NegMixin,
    PosMixin,
):
    """Celé číslo — aritmetika + bitwise"""
    __slots__ = ()


AddSubMulDivFloordivModPowAndOrXorInvertLshiftRshiftIntIndexAbsNegPosMixin = IntegerMixin
