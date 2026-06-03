from .atoms import ContainsMixin, LenMixin

class ContainerMixin(ContainsMixin, LenMixin):
    """Objekt který umí `in` a `len()`"""
    __slots__ = ()

ContainsLenMixin = ContainerMixin