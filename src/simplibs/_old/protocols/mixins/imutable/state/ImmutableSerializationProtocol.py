from typing import Protocol, runtime_checkable, Any, Self
# Outers
from ...common.core_logic import SerializationBaseProtocol, SnapshotProtocol


@runtime_checkable
class ImmutableSerializationProtocol(SerializationBaseProtocol, SnapshotProtocol, Protocol):
    """
    Protokol pro mixin ImmutableSerialization.

    Garantuje rozhraní pro funkcionální (imutabilní) rekonstrukci a aktualizaci
    stavu. Žádná z metod nemění původní instanci, ale vždy vrací novou instanci (Self).
    """

    def from_dict(self, user_dict: dict[str, Any]) -> Self:
        """
        Vytvoří a vrátí zcela novou imutabilní instanci naplněnou daty ze slovníku.
        Původní instance zůstává nezměněna.
        """
        ...

    def from_json(self, json_str: str) -> Self:
        """
        Odekóduje JSON řetězec a vrátí novou imutabilní instanci s těmito daty.
        """
        ...

    def update_constants(self, user_dict: dict[str, Any]) -> Self:
        """
        Vrátí novou imutabilní instanci, ve které jsou aktualizovány pouze konstantní
        (atomické) prvky podle předaného (i částečného) slovníku.
        """
        ...

    def update(self, mapping: dict[str, Any]) -> Self:
        """
        Ergonomický alias pro metodu from_dict. Vrací novou imutabilní instanci.
        """
        ...