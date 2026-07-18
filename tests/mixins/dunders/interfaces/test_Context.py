from typing import Literal, TYPE_CHECKING
from types import TracebackType
# Outers
from ...base_class import SimpleMixin
# Annotations
if TYPE_CHECKING:
    from ....protocols.mixins.dunders.interfaces import ContextProtocol


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

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice slotů
    __slots__ = ()

    # ----------------------------------------
    # Methods - ENTER / EXIT
    # ----------------------------------------

    def __enter__(
        self: "ContextProtocol"
    ) -> "ContextProtocol":
        """
        Vrací instanci při vstupu do kontextu.

        Umožňuje konstrukci:
            with obj as x:
                ...

        Bez jakékoli změny stavu instance.
        """
        return self

    def __exit__(
        self: "ContextProtocol",
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None
    ) -> Literal[False]:
        """
        Ukončuje kontextový blok.

        Vrací False, což znamená, že případné výjimky NEJSOU potlačeny
        a normálně se propagují dál. Mixin neprovádí žádné čištění ani
        změny stavu — je čistě syntaktický.
        """
        return False
