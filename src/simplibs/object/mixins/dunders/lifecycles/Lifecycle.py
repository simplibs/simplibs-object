# Inners
from .PickleReduce import PicleReduce
from .Copyable import Copyable


class Lifecycle(Copyable, PicleReduce):
    """
    Poskytuje implementaci Lifecycle  spojující všechny potřebné mixniy.
    """

    __slots__ = ()


