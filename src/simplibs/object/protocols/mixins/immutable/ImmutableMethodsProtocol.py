from typing import Protocol, runtime_checkable, Any, Self, TYPE_CHECKING
# outers
from ..core_mixins import InfrastructureProtocol
# Annotations
if TYPE_CHECKING:
    from ...alias_typings import ChangesTuple, ChangesDict



@runtime_checkable
class ImmutableMethodsProtocol(
    InfrastructureProtocol,
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
    _constant_names_tuple: set[str]

    # --- IMMUTABLE API - CORE ---

    def with_constants(
        self,
        changes_tuple: "ChangesTuple" = None
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

    def with_changes(self, changes_dict: "ChangesDict") -> Self:
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