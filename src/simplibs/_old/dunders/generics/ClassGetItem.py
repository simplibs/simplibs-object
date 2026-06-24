class ClassGetItem:
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

    __slots__ = ()

    @classmethod
    def __class_getitem__(cls, item):
        """
        Umožňuje zápis MyClass[T] bez nutnosti dědit z typing.Generic.

        Pokud nadřazená třída implementuje __class_getitem__, použije se její
        implementace. Pokud ne, vrací se samotná třída, což je standardní
        fallback používaný v Pythonu pro jednoduché generické zápisy.
        """
        try:
            return super().__class_getitem__(item)
        except Exception:
            return cls
