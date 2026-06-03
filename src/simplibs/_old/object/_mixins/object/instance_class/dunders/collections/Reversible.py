# class Reversible(IterMixin, ReversedMixin):
#     """Objekt který umí `for x in reversed(obj)`"""
#     __slots__ = ()

from .atoms import IterMixin, ReversedMixin


class ReversibleMixin(IterMixin, ReversedMixin):
    """Objekt který umí `for x in reversed(obj)`"""
    __slots__ = ()


IterReversedMixin = ReversibleMixin
