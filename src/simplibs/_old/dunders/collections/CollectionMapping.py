# Outers
from ...core_logic import CollectionBase


class CollectionMapping(CollectionBase):
    """
    Dict‑like API pro composite instance.
    Poskytuje přístup přes obj[key], nastavování hodnot a kontrolu existence.
    """

    # Definice určení
    _composite_only = True

    # Definice slotů
    __slots__ = ()

    def __len__(self) -> int:
        """Vrací počet přímých innerů."""
        return len(self._inners_name_tuple)

    def __contains__(self, key: str) -> bool:
        """Vrací True, pokud composite obsahuje inner s daným klíčem."""
        return key in self._inners_name_set

    def __missing__(self, key: str):
        """Vyvolá KeyError s informací o dostupných klíčích."""
        raise KeyError(
            f"Prvek '{key}' není definován v {self.meta.class_name}. "
            f"Dostupné prvky: {self.keys()}"
        )

    def __getitem__(self, key: str):
        """Vrací hodnotu inneru podle klíče, nebo vyvolá __missing__."""
        if key not in self._inners_name_set:
            self.__missing__(key)
        return getattr(self, key)

    def get(self, key: str, default=None):
        """Bezpečně vrací hodnotu inneru, nebo default pokud klíč neexistuje."""
        if key not in self._inners_name_set:
            return default
        return getattr(self, key)

    def __setitem__(self, key: str, value):
        """Nastaví hodnotu inneru podle klíče, pokud existuje."""

        # Kontrola zda nejsem na immutable objektu
        if not self.__mutable__:
            raise TypeError(
                f"Immutable composite '{self.meta.class_name}' "
                f"neumožňuje měnit hodnoty přes __setitem__."
            )

        # Kontrola zda klíč existuje
        if key not in self._inners_name_set:
            self.__missing__(key)

        # Požadavek na změnu hodnoty
        # (Může bý blokován na kompozici která mnemá dekompozici - v tu chvíli se vyhodí výjimka)
        setattr(self, key, value)
