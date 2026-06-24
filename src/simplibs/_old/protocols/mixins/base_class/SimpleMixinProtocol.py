from typing import Protocol, runtime_checkable


@runtime_checkable
class SimpleMixinProtocol(Protocol):
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

    # --- INICIALIZAČNÍ LOGIKA ---
    def init_mixins(self) -> None:
        """
        Kotva pro reaktivní inicializaci mixinů.

        V implementaci se očekává volání super().init_mixins(), které
        předá řízení dalšímu mixinu nebo bázové třídě v MRO řetězci.
        """
        ...