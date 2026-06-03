# class MappingView(GetitemMixin, IterMixin, LenMixin, ContainsMixin, ItemsKeysValuesMixin):
#     """Mapping s metodami .items(), .keys(), .values()"""
#     __slots__ = ()


from .atoms import (
    GetitemMixin,
    IterMixin,
    LenMixin,
    ContainsMixin,
    ItemsMixin,
    KeysMixin,
    ValuesMixin,
)


class MappingViewMixin(
    GetitemMixin,
    IterMixin,
    LenMixin,
    ContainsMixin,
    ItemsMixin,
    KeysMixin,
    ValuesMixin,
):
    """Mapping s metodami .items(), .keys(), .values()"""
    __slots__ = ()


GetitemIterLenContainsItemsKeysValuesMixin = MappingViewMixin
