from .Callable import CallableMixin
from .ContextManager import ContextManagerMixin

__all__ = (
    "CallableMixin",
    "ContextManagerMixin",
)


# # protocols/__init__.py
#
# # 1. Callable — volatelný objekt
# class Callable(CallMixin):
#     """Podporuje obj()"""
#     __slots__ = ()
#
# # 2. ContextManager — context manager
# class ContextManager(EnterMixin, ExitMixin):
#     """Podporuje `with obj:`"""
#     __slots__ = ()
