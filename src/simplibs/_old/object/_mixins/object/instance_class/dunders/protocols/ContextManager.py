# class ContextManager(EnterMixin, ExitMixin):
#     """Podporuje `with obj:`"""
#     __slots__ = ()

from .atoms import EnterMixin, ExitMixin


class ContextManagerMixin(
    EnterMixin,
    ExitMixin,
):
    """Podporuje `with obj:`"""
    __slots__ = ()


EnterExitMixin = ContextManagerMixin
