import json
# Inners
from .NodesTuple import NodesTuple
from ._utils.serialization import to_dict, from_dict, from_dict_constants


# noinspection PyAttributeOutsideInit
class Serialization(NodesTuple):
    """
    Poskytuje serializaci instance do dict/JSON a obnovu z nich.
    Základ pro HistoryMixin.
    """

    # -------------------------
    # Serializace
    # -------------------------
    def to_dict(self, *, constant_only: bool = False) -> dict:
        """Serializuje instanci do čitelného dict."""
        return to_dict(self, constant_only=constant_only)

    def to_json(self, **kwargs) -> str:
        """Serializuje instanci do JSON."""
        return json.dumps(self.to_dict(), ensure_ascii=False, **kwargs)

    # -------------------------
    # Obnova
    # -------------------------
    def from_dict(self, data: dict):
        """Vytvoří instanci z dict."""
        return from_dict(self, data)

    def from_json(self, json_str: str):
        """Vytvoří instanci z JSON."""
        return self.from_dict(json.loads(json_str))

    def update_constants(self, data: dict):
        """Aktualizuje konstanty z dict."""
        return from_dict_constants(self, data)


