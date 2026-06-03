from .atoms import GetitemMixin, IterMixin, LenMixin, ContainsMixin

class MappingMixin(GetitemMixin, IterMixin, LenMixin, ContainsMixin):
    """Read-only mapping (obj['key'], len, in, iteration)"""
    __slots__ = ()

GetitemIterLenContainsMixin = MappingMixin