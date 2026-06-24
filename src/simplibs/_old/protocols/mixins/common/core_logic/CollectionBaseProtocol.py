from typing import Protocol, runtime_checkable
# outers
from ....types import SimpleInstanceType


@runtime_checkable
class CollectionBaseProtocol(SimpleInstanceType, Protocol):
    """
    Protokol pro mixin CollectionBase.

    Garantuje základní mapovací API pro kompozitní instance (O(1) lookupy
    a deterministické řazení klíčů podle blueprintu).
    """

    # --- TECHNICKÉ ATRIBUTY (Inicializované v init_mixins) ---
    _inners_name_set: set[str]
    _inners_name_tuple: tuple[str, ...]

    # --- VEŘEJNÉ MAPOVACÍ API ---
    def keys(self) -> list[str]:
        """Vrací seznam klíčů (name_snake) všech přímých vnitřních prvků (inners)."""
        ...

    def values(self) -> list[object]:
        """Vrací seznam hodnot odpovídajících jednotlivým vnitřním prvkům (inners)."""
        ...

    def items(self) -> list[tuple[str, object]]:
        """Vrací seznam dvojic (klíč, hodnota) pro všechny vnitřní prvky (inners)."""
        ...