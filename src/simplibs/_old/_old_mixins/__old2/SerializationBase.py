import json
# Inners
from .NodesTuple import NodesTuple
from ._utils.serialization import to_dict


# noinspection PyAttributeOutsideInit
class SerializationBase(NodesTuple):
    """
    Společná serializační logika:
    - to_dict()
    - to_json()

    Bez jakékoli mutace instance.
    """

    def to_dict(self, *, constant_only: bool = False) -> dict:
        """Serializuje instanci do čitelného dict."""
        return to_dict(self, constant_only=constant_only)

    def to_json(self, **kwargs) -> str:
        """Serializuje instanci do JSON."""
        return json.dumps(self.to_dict(), ensure_ascii=False, **kwargs)
