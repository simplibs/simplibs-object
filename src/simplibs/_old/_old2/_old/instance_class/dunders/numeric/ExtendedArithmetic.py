# class ExtendedArithmetic(AddMixin, SubMixin, MulMixin, DivMixin, FloordivMixin, ModMixin, PowMixin):
#     """Podporuje +, -, *, /, //, %, **"""
#     __slots__ = ()

from .atoms import (
    AddMixin,
    SubMixin,
    MulMixin,
    DivMixin,
    FloordivMixin,
    ModMixin,
    PowMixin,
)


class ExtendedArithmeticMixin(
    AddMixin,
    SubMixin,
    MulMixin,
    DivMixin,
    FloordivMixin,
    ModMixin,
    PowMixin,
):
    """Podporuje +, -, *, /, //, %, **"""
    __slots__ = ()


AddSubMulDivFloordivModPowMixin = ExtendedArithmeticMixin
