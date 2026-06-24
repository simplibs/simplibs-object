# Outers
from ..._shared_logic.immutability import with_any
from ...core_mixins import NodesDicts, Snapshot


class Call(NodesDicts, Snapshot):
    """
    Mixin poskytující podporu pro volání instance jako funkce (`obj(...)`).

    Tento mixin slouží jako syntaktická nadstavba nad immutable API.
    Umožňuje zadávat změny pomocí tuple zápisu:

        obj("a", 10)
        obj(("a", 10), ("b", 20))
        obj((("a", 10), ("b", 20)))

    Logika:
    - Veškeré zpracování deleguje na interní engine `with_any`.
    - Nepřidává žádnou vlastní validaci ani logiku.
    - Je univerzální pro mutable i immutable objekty.
    """

    __slots__ = ()

    def __call__(self, *changes, **kwargs):
        """
        Umožňuje volat instanci jako funkci.

        Podporované formy:
            obj("a", 10)
            obj(("a", 10))
            obj(("a", 10), ("b", 20))
            obj((("a", 10), ("b", 20)))

        Pokud jsou použity keyword argumenty, převedou se na tuple formu.
        """

        # 1) Pokud jsou použity keyword argumenty → převedeme je na tuple
        if kwargs:
            # kwargs mají vždy formu konstant
            changes = tuple(kwargs.items())

        # 2) Pokud je předán jediný tuple → sjednotíme formu
        elif len(changes) == 1 and isinstance(changes[0], tuple):
            changes = changes[0]

        # 3) Delegace na engine
        return with_any(self, changes)
