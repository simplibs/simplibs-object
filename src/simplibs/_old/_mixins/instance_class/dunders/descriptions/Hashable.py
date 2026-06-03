# class Hashable(HashMixin):
#     """Objekt použitelný v set/dict (má __hash__)"""
#     __slots__ = ()

from .atoms import HashMixin


HashableMixin = HashMixin
