from typing import Protocol, runtime_checkable, Any, TYPE_CHECKING
# Outers
from ...core_mixins import SerializationProtocol
# Annotations
if TYPE_CHECKING:
    from ....alias_typings import StateDict


@runtime_checkable
class PickleStateProtocol(
    SerializationProtocol,
    Protocol
):
    """
    Protokol pro mixin PickleState.

    Garantuje podporu pro ukládání a obnovu stavu objektu (mrazení/tání)
    pomocí standardního Python pickle protokolu skrze slovníkovou reprezentaci.
    """

    def __getstate__(self) -> "StateDict":
        """
        Exportuje kompletní aktuální stav instance ve formě čistého slovníku.
        Využívá k tomu interně metodu to_dict().
        """
        ...

    def __setstate__(self, state: "StateDict") -> None:
        """
        Obnoví vnitřní stav instance z předaného slovníku.
        Vyžaduje a volá metodu from_dict(), jinak vyvolá TypeError.
        """
        ...

    # --- POŽADOVANÉ ROZHRANÍ PRO SPRÁVNOU FUNKCI MIXINU ---

    def from_dict(self, user_dict: "StateDict") -> Any:
        """
        Metoda, kterou tento mixin pro svou správnou funkci striktně vyžaduje
        na cílové třídě (implementováno přes Mutable/ImmutableSerialization).
        """
        ...