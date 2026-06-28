from typing import TYPE_CHECKING
# Outers
from ...base_class import SimpleMixin
# Annotations
if TYPE_CHECKING:
    from ....protocols.mixins.dunders import CollectionBaseProtocol
    from ....protocols.alias_typings import NamesSet, NamesTuple


class CollectionBase(SimpleMixin):
    """
    Základní mapovací mixin pro composite instance.
    Vytváří zmrazený slovník {name_snake: inner_instance} a poskytuje
    základní API keys(), values(), items().
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice určení
    _composite_only = True

    # Definice slotů
    __slots__ = ("_inners_name_set", "_inners_name_tuple")

    # ----------------------------------------
    # Hook pro inicializaci
    # ----------------------------------------

    # noinspection PyAttributeOutsideInit
    def init_mixins(
        self: "CollectionBaseProtocol"
    ) -> None:
        """
        Inicializuje dvě neměnné struktury pro práci s inners:

        - `_inners_name_tuple`: n-tice všech name_snake klíčů v deterministickém
          pořadí podle definice blueprintu. Slouží jako zdroj pro iteraci,
          reversed(), keys(), values() a items().

        - `_inners_name_set`: množina všech name_snake klíčů. Slouží pro rychlé
          ověřování existence klíče (O(1) lookup).

        Obě struktury jsou odvozené pouze z přímých innerů a jsou neměnné po celou
        dobu životního cyklu instance.
        """

        # 1. Inicializace předků
        super().init_mixins()

        # 2. Tuple držící name_snake v přesném pořadí
        self._inners_name_tuple: "NamesTuple" = tuple(
            inner.meta.name_snake
            for inner in self.meta.inners
        )

        # 3. Set pro rychlé porovnání přístomnosti
        self._inners_name_set: "NamesSet" = set(self._inners_name_tuple)

    # ----------------------------------------
    # Methods - KEYS / VALUES / ITEMS
    # ----------------------------------------

    def keys(
        self: "CollectionBaseProtocol"
    ) -> list[str]:
        """Vrací seznam klíčů (name_snake) všech přímých innerů."""
        return list(self._inners_name_tuple)

    def values(
        self: "CollectionBaseProtocol"
    ) -> list[object]:
        """Vrací seznam hodnot odpovídajících jednotlivým innerům."""
        return [
            getattr(self, key)
            for key in self._inners_name_tuple
        ]

    def items(
        self: "CollectionBaseProtocol"
    ) -> list[tuple[str, object]]:
        """Vrací seznam dvojic (klíč, hodnota) pro všechny innery."""
        return [
            (key, getattr(self, key))
            for key in self._inners_name_tuple
        ]
