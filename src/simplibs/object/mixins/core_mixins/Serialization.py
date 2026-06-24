import json
# Inners
from .NodesTuple import NodesTuple
from ._utils.serialization import to_dict, from_dict, from_dict_constants


class Serialization(NodesTuple):
    """
    Univerzální master mixin pro kompletní serializaci a deserializaci objektu.

    Zastřešuje export (to_dict, to_json) i import (from_dict, from_json, update).
    Díky vestavěnému uzavřenému typovému systému automaticky reaguje na to,
    zda objekt operuje v mutable režimu (mutace in-place) nebo immutable
    režimu (vrací upravenou novou instanci).
    """

    __slots__ = ()

    # ---------------------------------------------------------
    # 1) EXPORT (Původní SerializationBase)
    # ---------------------------------------------------------
    def to_dict(self, *, constant_only: bool = False) -> dict:
        """Serializuje instanci do čitelného plochého slovníku."""
        return to_dict(self, constant_only=constant_only)

    def to_json(self, **kwargs) -> str:
        """Serializuje instanci do formátu JSON řetězce."""
        return json.dumps(self.to_dict(), ensure_ascii=False, **kwargs)

    # ---------------------------------------------------------
    # 2) IMPORT / AKTUALIZACE (Společné pro oba světy)
    # ---------------------------------------------------------
    def from_dict(self, user_dict: dict):
        """
        Zrekonstruuje stav instance z předaného slovníku.

        - V mutable režimu: Modifikuje instanci přímo na místě (in-place).
        - V immutable režimu: Vrací novou upravenou instanci.
        """
        return from_dict(self, user_dict)

    def from_json(self, json_str: str):
        """Zrekonstruuje stav instance z JSON řetězce."""
        return self.from_dict(json.loads(json_str))

    def update_constants(self, user_dict: dict):
        """
        Aktualizuje konstanty (atomy) z předaného slovníku.
        Slovník může být částečný. Respektuje mutable/immutable režim.
        """
        return from_dict_constants(self, user_dict)
