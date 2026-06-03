# class Persistent(CopyMixin, DeepcopyMixin, GetstateMixin, SetstateMixin, ReduceMixin):
#     """Plná podpora kopírování i serializace"""
#     __slots__ = ()

from .atoms import (
    CopyMixin,
    DeepcopyMixin,
    GetstateMixin,
    SetstateMixin,
    ReduceMixin,
)


class PersistentMixin(
    CopyMixin,
    DeepcopyMixin,
    GetstateMixin,
    SetstateMixin,
    ReduceMixin,
):
    """Plná podpora kopírování i serializace"""
    __slots__ = ()


CopyDeepcopyGetstateSetstateReduceMixin = PersistentMixin
