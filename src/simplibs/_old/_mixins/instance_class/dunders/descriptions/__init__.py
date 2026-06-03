from .Hashable import HashableMixin
from .Printable import PrintableMixin
from .Representable import RepresentableMixin
from .Formattable import FormattableMixin
from .Convertible import ConvertibleMixin

__all__ = (
    "HashableMixin",
    "PrintableMixin",
    "RepresentableMixin",
    "FormattableMixin",
    "ConvertibleMixin",
)


# # descriptions/__init__.py
#
# # 1. Hashable — jen hash
# class Hashable(HashMixin):
#     """Objekt použitelný v set/dict (má __hash__)"""
#     __slots__ = ()
#
# # 2. Representable — string reprezentace
# class Representable(ReprMixin, StrMixin):
#     """Objekt má __repr__ a __str__"""
#     __slots__ = ()
#
# # 3. Printable — Representable + Bool
# class Printable(ReprMixin, StrMixin, BoolMixin):
#     """Representable + __bool__"""
#     __slots__ = ()
#
# # 4. Formattable — Printable + Format
# class Formattable(ReprMixin, StrMixin, BoolMixin, FormatMixin):
#     """Plná reprezentace včetně f-stringů"""
#     __slots__ = ()
#
# # 5. Convertible — binární konverze
# class Convertible(BytesMixin):
#     """Podporuje bytes(obj)"""
#     __slots__ = ()
#
#
# # **Poznámka:** `Hashable` **samostatně**, protože hash se často kombinuje s `Equality`, ne s representation.
