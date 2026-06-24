from typing import Protocol, runtime_checkable, Any
# Inners
from .NodesTupleProtocol import NodesTupleProtocol


@runtime_checkable
class SerializationBaseProtocol(NodesTupleProtocol, Protocol):
    """
    Protokol pro mixin SerializationBase.

    Definuje veřejné bezpečné rozhraní pro serializaci vnitřního stavu
    celé hierarchie prvků do formátů dict a JSON.
    """

    def to_dict(self, *, constant_only: bool = False) -> dict[str, Any]:
        """
        Serializuje instanci a její vnitřní prvky do čistého slovníku.
        Umožňuje odfiltrovat pouze konstantní (atomické) hodnoty.
        """
        ...

    def to_json(self, **kwargs: Any) -> str:
        """
        Serializuje instanci do formátu JSON řetězce.
        Přijímá volitelné parametry pro vestavěnou funkci json.dumps (např. indent).
        """
        ...