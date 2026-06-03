# class Arithmetic(AddMixin, SubMixin, MulMixin, DivMixin):
#     """Podporuje +, -, *, /"""
#     __slots__ = ()

from .atoms import AddMixin, SubMixin, MulMixin, DivMixin


class ArithmeticMixin(
    AddMixin,
    SubMixin,
    MulMixin,
    DivMixin,
):
    """Podporuje +, -, *, /"""
    __slots__ = ()


AddSubMulDivMixin = ArithmeticMixin
