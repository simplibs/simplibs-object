# Inners
from .Iterable import Iterable
from .Mapping import Mapping


class Collection(Iterable, Mapping):
    """
    Kompletní kolekční chování pro composite instance.
    Kombinuje iteraci i dict‑like API.
    """

    # Definice určení
    _composite_only = True

    # Definice slotů
    __slots__ = ()
