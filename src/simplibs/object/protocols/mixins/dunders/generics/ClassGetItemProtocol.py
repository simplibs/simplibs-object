from typing import Protocol, runtime_checkable, Any
# Outers
from ...base_class import SimpleMixinProtocol


@runtime_checkable
class ClassGetItemProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protokol pro mixin ClassGetItem.

    Garantuje podporu pro generickou indexaci na úrovni třídy (např. MojeTrida[int]),
    což umožňuje čisté používání pokročilých type hints bez runtime penalizace.
    """

    def __class_getitem__(cls, item: Any) -> type:
        """
        Speciální dunder metoda pro podporu generické syntaxe na třídě.
        Vrací buď výsledek nadřazené třídy, nebo samotný class objekt (type).
        """
        ...