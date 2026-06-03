# class Copyable(CopyMixin, DeepcopyMixin):
#     """Podporuje copy() a deepcopy()"""
#     __slots__ = ()

from .atoms import CopyMixin, DeepcopyMixin


class CopyableMixin(
    CopyMixin,
    DeepcopyMixin,
):
    """Podporuje copy() a deepcopy()"""
    __slots__ = ()


CopyDeepcopyMixin = CopyableMixin
