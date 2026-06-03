# class MutableMapping(SetitemMixin, GetitemMixin, IterMixin, LenMixin, ContainsMixin):
#     """Mutable mapping (obj['key'] = value)"""
#     __slots__ = ()

from .atoms import (
    SetitemMixin,
    GetitemMixin,
    IterMixin,
    LenMixin,
    ContainsMixin,
)


class MutableMappingMixin(
    SetitemMixin,
    GetitemMixin,
    IterMixin,
    LenMixin,
    ContainsMixin,
):
    """Mutable mapping (obj['key'] = value)"""
    __slots__ = ()


SetitemGetitemIterLenContainsMixin = MutableMappingMixin
