import json
# Outers
from ...common.core_logic import SerializationBase, Snapshot
from ....protocols import SimpleInstanceType
# Inners
from ._utils.serialization import from_dict, from_dict_constants


class ImmutableSerialization(SerializationBase, Snapshot):
    """
    Immutable serializace:
    - from_dict_immutable()
    - from_json_immutable()
    - update_constants_immutable()

    Vždy vrací NOVOU instanci.
    """

    # Definice určení
    _immutable_only = True

    def from_dict(self: SimpleInstanceType, user_dict: dict) -> SimpleInstanceType:
        """Vytvoří novou immutable instanci z dict."""
        return from_dict(self, user_dict)

    def from_json(self: SimpleInstanceType, json_str: str) -> SimpleInstanceType:
        """Vytvoří novou immutable instanci z JSON řetězce."""
        return self.from_dict_immutable(json.loads(json_str))

    def update_constants(self: SimpleInstanceType, user_dict: dict) -> SimpleInstanceType:
        """
        Vrací novou instanci s aktualizovanými konstantami.
        Dict může být částečný – použijí se jen nalezené konstanty.
        """
        return from_dict_constants(self, user_dict)

    def update(self, mapping: dict):
        """Hromadně aktualizuje hodnoty innerů - alias pro metodu from_dict."""
        return self.from_dict(mapping)