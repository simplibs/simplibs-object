from typing import Protocol, runtime_checkable, Any
# Outers
from ...base_class import SimpleMixinProtocol


@runtime_checkable
class EqualityProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protokol pro mixin Equality.

    Garantuje schopnost porovnávání instancí na rovnost (hodnotovou i objektovou)
    a poskytuje bezpečnou, dynamickou hashovací strategii reagující na stav mutability.
    """

    def __eq__(self, other: Any) -> bool:
        """
        Porovná instanci s jiným objektem na rovnost.
        Vrací True, pokud se shodují hodnoty (a případně i blueprinty), jinak False.
        """
        ...

    def __hash__(self) -> int:
        """
        Vrací unikátní číselný hash instance.
        Pro mutable objekty generuje hash z identity id(self),
        pro immutable z hodnoty hash(self.value).
        """
        ...