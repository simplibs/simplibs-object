from typing import Protocol, runtime_checkable, Any, Self
# Inners
from .NodesTupleProtocol import NodesTupleProtocol


@runtime_checkable
class SerializationProtocol(
    NodesTupleProtocol,
    Protocol
):
    """
    Protokol pro univerzální master mixin Serialization.

    Garantuje kompletní sadu metod pro export (to_dict, to_json) a 
    import/aktualizaci (from_dict, from_json, update_constants, update) dat objektu.
    Bezpečně pokrývá jak in-place mutace, tak immutable transformace.
    """

    # ---------------------------------------------------------
    # 1) EXPORT (Exportní API)
    # ---------------------------------------------------------
    def to_dict(self, *, constant_only: bool = False) -> dict[str, Any]:
        """Serializuje instanci do čitelného plochého slovníku."""
        ...

    def to_json(self, **kwargs: Any) -> str:
        """Serializuje instanci do formátu JSON řetězce."""
        ...

    # ---------------------------------------------------------
    # 2) IMPORT / AKTUALIZACE (Importní API s podporou Fluent API)
    # ---------------------------------------------------------
    def from_dict(self, user_dict: dict[str, Any]) -> Self:
        """
        Zrekonstruuje stav instance z předaného slovníku.
        Vrací instanci (Self) pro možnost řetězení metod.
        """
        ...

    def from_json(self, json_str: str) -> Self:
        """
        Zrekonstruuje stav instance z JSON řetězce.
        Vrací instanci (Self) pro možnost řetězení metod.
        """
        ...

    def update_constants(self, user_dict: dict[str, Any]) -> Self:
        """
        Aktualizuje konstanty (atomy) z předaného částečného nebo úplného slovníku.
        Vrací instanci (Self) pro možnost řetězení metod.
        """
        ...
