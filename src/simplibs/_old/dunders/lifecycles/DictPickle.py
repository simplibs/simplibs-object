# Outers
from ...core_logic import SerializationBase


class DictPickle(SerializationBase):
    """
    Mixin poskytující pickle/unpickle chování založené na to_dict()/from_dict().

    Tento mixin implementuje dundery __getstate__ a __setstate__ tak, aby
    serializace probíhala přes čitelný dict (to_dict) a deserializace přes
    metodu from_dict. Díky tomu je pickle stabilní, čitelný a nezávislý na
    interní reprezentaci objektu.

    Podmínky použití:
    - Třída MUSÍ poskytovat metodu from_dict() (MutableSerialization nebo
      ImmutableSerialization).
    - Mixin funguje jak pro mutable instance (mutace in-place), tak pro
      immutable instance (from_dict vrací novou instanci, kterou pickle
      automaticky použije).
    """

    __slots__ = ()

    def __getstate__(self) -> dict:
        """
        Vrací stav instance jako dict pomocí to_dict().

        Pickle tento dict uloží jako reprezentaci objektu. Výhodou je, že
        serializace je stabilní, čitelná a nezávislá na interních a privátních
        atributech instance.
        """
        return self.to_dict()

    def __setstate__(self, state: dict) -> None:
        """
        Obnoví stav instance z dictu pomocí from_dict().

        Kontroluje, zda třída poskytuje metodu from_dict(). Pokud ne, vyvolá
        TypeError s jasným vysvětlením. Pro mutable instance se stav obnoví
        přímo do self. Pro immutable instance from_dict() vrací novou instanci,
        kterou pickle automaticky použije jako výsledný objekt.
        """
        if not hasattr(self.__class__, "from_dict"):
            raise TypeError(
                f"{self.__class__.__name__} requires a from_dict() method "
                f"(provided by MutableSerialization or ImmutableSerialization)."
            )

        self.from_dict(state)
