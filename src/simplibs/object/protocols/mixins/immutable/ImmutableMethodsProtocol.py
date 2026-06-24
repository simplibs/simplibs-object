from typing import Protocol, runtime_checkable, Any, Self
# outers
from ..core_mixins import NodesDictsProtocol, SnapshotProtocol


@runtime_checkable
class ImmutableMethodsProtocol(
    NodesDictsProtocol,
    SnapshotProtocol,
    Protocol
):
    """
    Protokol pro mixin ImmutableMethods.

    Garantuje kompletní sadu metod pro imutabilní (funkcionální) transformace stavu.
    Žádná z metod nemění stav stávající instance, nýbrž bezpečně produkuje
    novou upravenou instanci (Self).
    """

    # --- TECHNICKÉ ATRIBUTY (Inicializované v init_mixins) ---

    # Množina snake_case názvů všech vnitřních konstantních (atomických) prvků
    _constant_names: set[str]

    # --- IMMUTABLE API - CORE ---

    def with_constants(
        self,
        changes_tuple: tuple[str, Any] | tuple[tuple[str, Any], ...] | None = None
    ) -> Self:
        """
        Vytvoří a vrátí novou imutabilní instanci na základě jedné nebo více
        předaných změn v konstantních prvcích.
        """
        ...

    def with_constant(self, name: str, new_value: Any) -> Self:
        """
        Vytvoří a vrátí novou imutabilní instanci se změněnou hodnotou
        u jedné konkrétní konstanty (atomu) specifikované jejím názvem.
        """
        ...

    def with_composite(self, name: str, new_value: Any) -> Self:
        """
        Vytvoří a vrátí novou imutabilní instanci se změněnou hodnotou
        u jedné konkrétní kompozice specifikované jejím názvem.
        """
        ...

    # --- IMMUTABLE API - EXTENDED ---

    def with_changes(self, changes_dict: dict[str, Any]) -> Self:
        """
        Ergonomická metoda umožňující zadat mapování více změn pro konstanty
        ve formě standardního slovníku. Vrací novou imutabilní instanci.
        """
        ...

    def with_value(self, new_value: Any) -> Self:
        """
        Ergonomický alias pro změnu hlavní hodnoty celé této instance.
        Vrací novou imutabilní instanci.
        """
        ...

    def duplicate(self) -> Self:
        """
        Vytvoří a vrátí identickou novou kopii (duplikát) této imutabilní instance
        se zachováním kompletního aktuálního stavu.
        """
        ...