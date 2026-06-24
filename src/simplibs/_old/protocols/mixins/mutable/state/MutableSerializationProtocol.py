from typing import Protocol, runtime_checkable, Any
# Outers
from ...common.core_logic import SerializationBaseProtocol


@runtime_checkable
class MutableSerializationProtocol(SerializationBaseProtocol, Protocol):
    """
    Protokol pro mixin MutableSerialization.

    Rozšiřuje základní exportní serializaci o metody, které umožňují
    hromadný import, aktualizaci a rekonstrukci vnitřního stavu instance
    ze struktur dict a JSON.
    """

    def from_dict(self, user_dict: dict[str, Any]) -> None:
        """
        Naplní a zmutuje vnitřní stav instance a jejích prvků na základě dat ze slovníku.
        """
        ...

    def from_json(self, json_str: str) -> None:
        """
        Odekóduje JSON řetězec a předá data metodě from_dict pro mutaci stavu instance.
        """
        ...

    def update_constants(self, user_dict: dict[str, Any]) -> None:
        """
        Hromadně aktualizuje pouze konstantní (atomické) prvky v hierarchii na základě předaných dat.
        """
        ...

    def update(self, mapping: dict[str, Any]) -> None:
        """
        Hromadný alias pro metodu from_dict. Slouží pro ergonomickou aktualizaci inner prvků.
        """
        ...