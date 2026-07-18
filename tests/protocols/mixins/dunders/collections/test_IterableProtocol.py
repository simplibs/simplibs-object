from typing import Protocol, runtime_checkable
from collections.abc import Iterator
# Inners
from .CollectionBaseProtocol import CollectionBaseProtocol


@runtime_checkable
class IterableProtocol(
    CollectionBaseProtocol,
    Protocol
):
    """
    Protokol pro mixin CollectionIterable.

    Garantuje iterační rozhraní pro kompozitní objekty, podporu reverzního
    průchodu a rozšíření systémové introspekce dir().
    """

    def __iter__(self) -> Iterator[str]:
        """
        Vrací iterátor přes klíče (name_snake) všech přímých vnitřních prvků
        v pořadí definovaném v blueprintu.
        """
        ...

    def __reversed__(self) -> Iterator[str]:
        """
        Vrací iterátor pro průchod klíči vnitřních prvků v opačném pořadí.
        """
        ...

    def __dir__(self) -> list[str]:
        """
        Vrací seřazený seznam všech atributů a metod objektu,
        rozšířený o názvy všech vnitřních prvků (innerů).
        """
        ...