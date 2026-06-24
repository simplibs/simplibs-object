import json
# Outers
from ...common.core_logic import SerializationBase
# Inners
from ._utils.serialization import from_dict, from_dict_constants


class MutableSerialization(SerializationBase):
    """
    Mutable serializace:
    - from_dict()
    - from_json()
    - update_constants()

    Tyto metody MUTUJÍ instanci → patří do mutable systému.
    """

    # Definice určení
    _mutable_only = True

    def from_dict(self, user_dict: dict):
        """Vytvoří instanci z dict."""
        return from_dict(self, user_dict)

    def from_json(self, json_str: str):
        """Vytvoří instanci z JSON."""
        return self.from_dict(json.loads(json_str))

    def update_constants(self, user_dict: dict):
        """Aktualizuje konstanty z dict."""
        return from_dict_constants(self, user_dict)

    def update(self, mapping: dict):
        """Hromadně aktualizuje hodnoty innerů - alias pro metodu from_dict."""
        return self.from_dict(mapping)
