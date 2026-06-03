# class Formattable(ReprMixin, StrMixin, BoolMixin, FormatMixin):
#     """Plná reprezentace včetně f-stringů"""
#     __slots__ = ()

from .atoms import ReprMixin, StrMixin, BoolMixin, FormatMixin


class FormattableMixin(
    ReprMixin,
    StrMixin,
    BoolMixin,
    FormatMixin,
):
    """Plná reprezentace včetně f-stringů"""
    __slots__ = ()


ReprStrBoolFormatMixin = FormattableMixin

