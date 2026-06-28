from typing import Any, Self
# Outers
from ...base_class import SimpleMixin


class ClassGetItem(SimpleMixin):
    """
    Mixin poskytující podporu pro syntaxi generik typu:

        MyClass[int]
        MyClass[str]
        MyClass[tuple[int, str]]

    Tato metoda je čistě syntaktická pomůcka pro type hints, IDE a statickou
    analýzu. Nemá žádný vliv na runtime chování instance ani na konstrukci
    instanční třídy.

    Logika:
    - Pokud nadřazená třída (__class_getitem__) existuje, použije se.
    - Pokud neexistuje (což je běžné u běžných tříd), vrací se samotná třída.
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice slotů
    __slots__ = ()

    # ----------------------------------------
    # Classmethods - CLASS GETITEM
    # ----------------------------------------

    @classmethod
    def __class_getitem__(
        cls: type[Self],
        item: Any
    ) -> type[Self] | Any:
        """
        Umožňuje zápis MyClass[T] bez nutnosti dědit z typing.Generic.

        Pokud nadřazená třída implementuje __class_getitem__, použije se její
        implementace. Pokud ne, vrací se samotná třída, což je standardní
        fallback používaný v Pythonu pro jednoduché generické zápisy.
        """

        # 1. Načtení metody z nadřazené třídy
        super_cls = super(ClassGetItem, cls)
        method = getattr(super_cls, "__class_getitem__", None)

        # 2. Navrácení metody a nebo třídy jako fallbacku
        return (
            method(item)
            if method is not None
            else cls
        )
