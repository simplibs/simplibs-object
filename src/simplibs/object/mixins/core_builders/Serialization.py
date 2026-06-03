import json
# Outers
from ..base_class import SimpleMixin
from ..._utils.serializations import to_dict, from_dict


class Serialization(SimpleMixin):
    """
    Pohodlné metody pro převod instance na dict/JSON a zpět,
    postavené nad externími serializačními funkcemi.
    """

    __slots__ = ()

    def to_dict(self):
        """Serializuje instanci do dict."""
        return to_dict(self)

    @classmethod
    def from_dict(cls, data):
        """Vytvoří instanci ze serializovaného dictu."""
        return from_dict(cls, data)

    def to_json(self, **kwargs):
        """Serializuje instanci do JSON."""
        return json.dumps(self.to_dict(), ensure_ascii=False, **kwargs)

    @classmethod
    def from_json(cls, json_str):
        """Vytvoří instanci z JSON."""
        return cls.from_dict(json.loads(json_str))
