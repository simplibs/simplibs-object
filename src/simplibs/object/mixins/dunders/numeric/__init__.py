from .Numeric import NumericMixin
from .Arithmetic import ArithmeticMixin
from .ExtendedArithmetic import ExtendedArithmeticMixin
from .Bitwise import BitwiseMixin
from .Convertible import ConvertibleMixin
from .Integer import IntegerMixin
from .InPlaceNumeric import InPlaceNumericMixin

__all__ = (
    "NumericMixin",
    "ArithmeticMixin",
    "ExtendedArithmeticMixin",
    "BitwiseMixin",
    "ConvertibleMixin",
    "IntegerMixin",
    "InPlaceNumericMixin",
)


# # numeric/__init__.py
#
# # 1. Arithmetic — základní aritmetika
# class Arithmetic(AddMixin, SubMixin, MulMixin, DivMixin):
#     """Podporuje +, -, *, /"""
#     __slots__ = ()
#
# # 2. ExtendedArithmetic — vše včetně //, %, **
# class ExtendedArithmetic(AddMixin, SubMixin, MulMixin, DivMixin, FloordivMixin, ModMixin, PowMixin):
#     """Podporuje +, -, *, /, //, %, **"""
#     __slots__ = ()
#
# # 3. Bitwise — bitové operace
# class Bitwise(AndMixin, OrMixin, XorMixin, InvertMixin, LshiftMixin, RshiftMixin):
#     """Podporuje &, |, ^, ~, <<, >>"""
#     __slots__ = ()
#
# # 4. Numeric — aritmetika + konverze
# class Numeric(
#     AddMixin, SubMixin, MulMixin, DivMixin, FloordivMixin, ModMixin, PowMixin,
#     IntMixin, FloatMixin, AbsMixin, NegMixin, PosMixin
# ):
#     """Plné numerické chování"""
#     __slots__ = ()
#
# # 5. Integer — Numeric + Bitwise + Index
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
#
# # 6. InPlaceNumeric — mutující operace
# class InPlaceNumeric(IaddMixin, IsubMixin, ImulMixin, IdivMixin, IfloordivMixin, ImodMixin, IpowMixin):
#     """Podporuje +=, -=, *=, /=, //=, %=, **="""
#     __slots__ = ()
#
# # 7. Convertible — všechny konverze
# class Convertible(IntMixin, FloatMixin, ComplexMixin, CeilMixin, FloorMixin, RoundMixin, TruncMixin):
#     """Podporuje int(), float(), round(), atd."""
#     __slots__ = ()
#
#
# __DOCT__ = """
# # GROUP: `numeric/`
#
# > **Group purpose:**
# > All mathematical and bitwise operations. Python's numeric tower is expressed entirely
# > through dunders, which is why you can make any custom class behave as a number.
# > The group is subdivided by operation *kind*: binary arithmetic, in-place variants,
# > bitwise operations, unary operations, and type conversions.
# > Note: every binary operator also has a *reflected* variant (e.g., `__radd__`) that
# > Python calls when the left operand does not know how to handle the operation.
# > These reflected variants are not listed as separate atoms here because they follow
# > the exact same pattern; add them to each arithmetic atom as needed.
# """