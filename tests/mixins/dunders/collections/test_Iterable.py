from typing import TYPE_CHECKING
from collections.abc import Iterator
# Inners
from .CollectionBase import CollectionBase
# Annotations
if TYPE_CHECKING:
    from ....protocols.mixins.dunders.collections import IterableProtocol


class Iterable(CollectionBase):
    """
    Iterační API pro composite instance.
    Umožňuje iteraci, reverzní iteraci a rozšíření výpisu přes dir().
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice určení
    _composite_only = True

    # Definice slotů
    __slots__ = ()

    # ----------------------------------------
    # Methods - ITER / REVERSED / DIR
    # ----------------------------------------

    def __iter__(
        self: "IterableProtocol"
    ) -> Iterator[str]:
        """Iteruje přes klíče (name_snake) všech innerů v definovaném pořadí."""
        return iter(self._inners_name_tuple)

    def __reversed__(
        self: "IterableProtocol"
    ) -> Iterator[str]:
        """Vrací reverzní iterátor přes klíče innerů."""
        return reversed(self._inners_name_tuple)

    def __dir__(
        self: "IterableProtocol"
    ) -> list[str]:
        """Rozšiřuje výpis atributů o klíče innerů."""
        base = list(object.__dir__(self))
        base += list(self._inners_name_tuple)
        return sorted(set(base))
