# Outers
from ...core_logic import CollectionBase


class CollectionIterable(CollectionBase):
    """
    Iterační API pro composite instance.
    Umožňuje iteraci, reverzní iteraci a rozšíření výpisu přes dir().
    """

    # Definice určení
    _composite_only = True

    # Definice slotů
    __slots__ = ()

    def __iter__(self):
        """Iteruje přes klíče (name_snake) všech innerů v definovaném pořadí."""
        return iter(self._inners_name_tuple)

    def __reversed__(self):
        """Vrací reverzní iterátor přes klíče innerů."""
        return reversed(self._inners_name_tuple)

    def __dir__(self):
        """Rozšiřuje výpis atributů o klíče innerů."""
        base = list(object.__dir__(self))
        base += list(self._inners_name_tuple)
        return sorted(set(base))
