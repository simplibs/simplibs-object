from typing import Protocol, runtime_checkable, TYPE_CHECKING
# Outers
from ...instance import SimpleInstanceLike
# Annotations
if TYPE_CHECKING:
    from ...alias_typings import ValidTypes


@runtime_checkable
class SimpleMixinProtocol(
    SimpleInstanceLike,
    Protocol
):
    """
    Protokol reprezentující základní rozhraní pro všechny mixiny v systému Simple.

    Deklaruje přítomnost inicializační metody a konfiguračních flagů, které
    řídí, na jaké typy instancí smí být mixin v továrně aplikován.
    """

    # --- DEKLARATIVNÍ OMEZENÍ MIXINU (Třídní konfigurace) ---
    _constant_only: bool
    _composite_only: bool
    _mutable_only: bool
    _immutable_only: bool
    _only_types: "ValidTypes"

    # --- INICIALIZAČNÍ LOGIKA ---
    def init_mixins(self) -> None:
        """
        Kotva pro reaktivní inicializaci mixinů.

        V implementaci se očekává volání super().init_mixins(), které
        předá řízení dalšímu mixinu nebo bázové třídě v MRO řetězci.
        """
        ...

    @staticmethod
    def __extend_instance_class__(instance_cls: "SimpleInstanceLike") -> "SimpleInstanceLike":
        """
        Volitelný hook umožňující mixinu upravit instanční třídu
        před vytvořením runtime instance (např. přidat dynamické properties).
        """
        ...

    __name__: str
