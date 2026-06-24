# Inners
from .CollectionIterable import CollectionIterable
from .CollectionMapping import CollectionMapping


class Collection(CollectionIterable, CollectionMapping):
    """
    Kompletní kolekční chování pro composite instance.
    Kombinuje iteraci i dict‑like API.
    """

    # Definice určení
    _composite_only = True

    # Definice slotů
    __slots__ = ()
