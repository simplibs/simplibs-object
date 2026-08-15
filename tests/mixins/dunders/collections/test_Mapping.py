from typing import TYPE_CHECKING, Any
# Inners
from .CollectionBase import CollectionBase
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.dunders.collections import MappingProtocol


class Mapping(CollectionBase):
    """
    Dict‑like API pro composite instance.
    Poskytuje přístup přes obj[key], nastavování hodnot a kontrolu existence.
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice určení
    _composite_only = True

    # Definice slotů
    __slots__ = ()

    # ----------------------------------------
    # Methods - LEN / CONTAINS / MISSING
    # ----------------------------------------

    def __len__(
        self: "MappingProtocol"
    ) -> int:
        """Vrací počet přímých innerů."""
        return len(self._inners_name_tuple)

    def __contains__(
        self: "MappingProtocol",
        key: str
    ) -> bool:
        """Vrací True, pokud composite obsahuje inner s daným klíčem."""
        return key in self._inners_name_set

    def __missing__(
        self: "MappingProtocol",
        key: str
    ) -> None:
        """Vyvolá KeyError s informací o dostupných klíčích."""
        raise KeyError(
            f"Prvek '{key}' není definován v {self.meta.class_name}. "
            f"Dostupné prvky: {self.keys()}"
        )

    # ----------------------------------------
    # Methods - GETITEM / GET / SETITEM
    # ----------------------------------------

    def __getitem__(
        self: "MappingProtocol",
        key: str
    ):
        """Vrací hodnotu inneru podle klíče, nebo vyvolá __missing__."""
        if key not in self._inners_name_set:
            self.__missing__(key)
        return getattr(self, key)

    def get(
        self: "MappingProtocol",
        key: str,
        default: Any = None
    ):
        """Bezpečně vrací hodnotu inneru, nebo default pokud klíč neexistuje."""
        if key not in self._inners_name_set:
            return default
        return getattr(self, key)

    def __setitem__(
        self: "MappingProtocol",
        key: str,
        value: Any
    ):
        """Nastaví hodnotu inneru podle klíče, pokud existuje."""

        # 1. Kontrola zda nejsem na immutable objektu
        if not self.__is_mutable__:
            raise TypeError(
                f"Immutable composite '{self.meta.class_name}' "
                f"neumožňuje měnit hodnoty přes __setitem__."
            )

        # 2. Kontrola zda klíč existuje
        if key not in self._inners_name_set:
            self.__missing__(key)

        # 3. Požadavek na změnu hodnoty
        # (Může bý blokován na kompozici která mnemá dekompozici - v tu chvíli se vyhodí výjimka)
        setattr(self, key, value)
