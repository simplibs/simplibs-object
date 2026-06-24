from typing import Protocol, runtime_checkable, Any
# Inners
from .CollectionBaseProtocol import CollectionBaseProtocol


@runtime_checkable
class CollectionMappingProtocol(
    CollectionBaseProtocol,
    Protocol
):
    """
    Protokol pro mixin CollectionMapping.

    Garantuje slovníkové (Mapping) rozhraní pro kompozitní objekty,
    včetně čtení, zápisu, kontroly přítomnosti klíčů a bezpečného vyhledávání.
    """

    def __len__(self) -> int:
        """Vrací celkový počet přímých vnitřních prvků (innerů) v kompozici."""
        ...

    def __contains__(self, key: str) -> bool:
        """Vrací True, pokud kompozice obsahuje vnitřní prvek s daným klíčem (name_snake)."""
        ...

    def __missing__(self, key: str) -> None:
        """
        Vyvolá podrobný KeyError s informací o dostupných klíčích,
        pokud požadovaný vnitřní prvek v kompozici neexistuje.
        """
        ...

    def __getitem__(self, key: str) -> Any:
        """
        Vrací hodnotu vnitřního prvku podle jeho klíče.
        Pokud klíč neexistuje, deleguje řízení na metodu __missing__.
        """
        ...

    def get(self, key: str, default: Any = None) -> Any:
        """
        Bezpečně vrací hodnotu vnitřního prvku podle klíče.
        Pokud klíč neexistuje, vrací definovanou výchozí (default) hodnotu.
        """
        ...

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Nastaví novou hodnotu pro vnitřní prvek specifikovaný klíčem.
        Vyvolá TypeError u imutabilních objektů nebo KeyError, pokud klíč neexistuje.
        """
        ...