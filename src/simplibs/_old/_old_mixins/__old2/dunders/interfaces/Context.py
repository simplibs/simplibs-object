# Outers
from ....base_class import SimpleMixin


class ContextManager(SimpleMixin):
    """
    Mixin poskytující základní podporu pro kontextový manažer (`with obj:`).

    Tento mixin umožňuje použít instanci v konstrukci `with`, aniž by
    prováděl jakékoli vedlejší efekty. Je plně univerzální — funguje pro
    mutable i immutable objekty, pro atomy i kompozity, protože nijak
    nemění stav instance.

    Chování:
    - `__enter__` vrací instanci samotnou.
    - `__exit__` neignoruje výjimky (vrací False), takže případné chyby
      se normálně propagují dál.

    Tento mixin slouží čistě jako syntaktické rozšíření API a nezasahuje
    do logiky hodnot, snapshotů, mutability ani immutable režimu.
    """

    __slots__ = ()

    def __enter__(self):
        """
        Vrací instanci při vstupu do kontextu.

        Umožňuje konstrukci:
            with obj as x:
                ...

        Bez jakékoli změny stavu instance.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Ukončuje kontextový blok.

        Vrací False, což znamená, že případné výjimky NEJSOU potlačeny
        a normálně se propagují dál. Mixin neprovádí žádné čištění ani
        změny stavu — je čistě syntaktický.
        """
        return False
