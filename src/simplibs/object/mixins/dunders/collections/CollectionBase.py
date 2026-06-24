from types import MappingProxyType
# Outers
from ....protocols import SimpleInstanceType
from ...base_class import SimpleMixin


# noinspection PyAttributeOutsideInit
class CollectionBase(SimpleMixin):
    """
    Základní mapovací mixin pro composite instance.
    Vytváří zmrazený slovník {name_snake: inner_instance} a poskytuje
    základní API keys(), values(), items().
    """

    # Definice určení
    _composite_only = True

    # Definice slotů
    __slots__ = ("_inners_name_set", "_inners_name_tuple")

    # Inicializace mixinu
    def init_mixins(self: SimpleInstanceType):
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
        super().init_mixins()

        # Tuple držící name_snake v přesném pořadí
        self._inners_name_tuple = tuple(
            inner.meta.name_snake
            for inner in self.meta.inners
        )

        # Set pro rychlé porovnání přístomnosti
        self._inners_name_set = set(self._inners_name_tuple)


    def keys(self) -> list[str]:
        """Vrací seznam klíčů (name_snake) všech přímých innerů."""
        return list(self._inners_name_tuple)

    def values(self) -> list[object]:
        """Vrací seznam hodnot odpovídajících jednotlivým innerům."""
        return [
            getattr(self, key)
            for key in self._inners_name_tuple
        ]

    def items(self) -> list[tuple[str, object]]:
        """Vrací seznam dvojic (klíč, hodnota) pro všechny innery."""
        return [
            (key, getattr(self, key))
            for key in self._inners_name_tuple
        ]
