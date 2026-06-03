# class Serializable(GetstateMixin, SetstateMixin, ReduceMixin):
#     """Podporuje pickle (getstate, setstate, reduce)"""
#     __slots__ = ()

from .atoms import GetstateMixin, SetstateMixin, ReduceMixin


class SerializableMixin(
    GetstateMixin,
    SetstateMixin,
    ReduceMixin,
):
    """Podporuje pickle (getstate, setstate, reduce)"""
    __slots__ = ()


GetstateSetstateReduceMixin = SerializableMixin
