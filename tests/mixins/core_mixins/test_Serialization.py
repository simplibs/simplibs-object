from typing import TYPE_CHECKING
import json
# Inners
from .Infrastructure import Infrastructure
from ._utils.serialization import to_dict, from_dict, from_dict_constants
# Annotations
if TYPE_CHECKING:
    from ..._core.protocols.mixins.core_mixins import SerializationProtocol
    from ..._core.protocols.alias_typings import StateDict


class Serialization(Infrastructure):
    """
    Univerzální master mixin pro kompletní serializaci a deserializaci objektu.

    Zastřešuje export (to_dict, to_json) i import (from_dict, from_json, update).
    Díky vestavěnému uzavřenému typovému systému automaticky reaguje na to,
    zda objekt operuje v mutable režimu (mutace in-place) nebo immutable
    režimu (vrací upravenou novou instanci).
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice slotů
    __slots__ = ()

    # ----------------------------------------
    # Methods - EXPORT TO DICT / JSON
    # ----------------------------------------

    def to_dict(
        self: "SerializationProtocol",
        *,
        constant_only: bool = False
    ) -> "StateDict":
        """Serializuje instanci do čitelného plochého slovníku."""
        return to_dict(self, constant_only=constant_only)

    def to_json(
        self: "SerializationProtocol",
        **kwargs
    ) -> str:
        """Serializuje instanci do formátu JSON řetězce."""
        return json.dumps(self.to_dict(), ensure_ascii=False, **kwargs)

    # ----------------------------------------
    # Methods - IMPORT & AKTUALIZACE FROM DICT / JSON
    # ----------------------------------------

    def from_dict(
        self: "SerializationProtocol",
        user_dict: "StateDict"
    ) -> "SerializationProtocol":
        """
        Zrekonstruuje stav instance z předaného slovníku.

        - V mutable režimu: Modifikuje instanci přímo na místě (in-place).
        - V immutable režimu: Vrací novou upravenou instanci.
        """
        return from_dict(self, user_dict)

    def from_json(
        self: "SerializationProtocol",
        json_str: str
    ) -> "SerializationProtocol":
        """Zrekonstruuje stav instance z JSON řetězce."""
        return self.from_dict(json.loads(json_str))

    def update_constants(
        self: "SerializationProtocol",
        user_dict: "StateDict"
    ) -> "SerializationProtocol":
        """
        Aktualizuje konstanty (atomy) z předaného slovníku.
        Slovník může být částečný. Respektuje mutable/immutable režim.
        """
        return from_dict_constants(self, user_dict)
