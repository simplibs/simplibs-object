from typing import Protocol, Any, runtime_checkable, TYPE_CHECKING

# Annotations (Zabraňujeme cyklům, importujeme obecný zastřešující typ metadat)
if TYPE_CHECKING:
    from ..metadata import SimpleObjectMetadataProtocol


@runtime_checkable
class SimpleInstanceProtocol(Protocol):
    """
    Kořenový protokol pro všechny runtime instance v systému Simple.

    Zastřešuje společné technické dundery vštěpované tovární funkcí `create_instance`
    a garantuje přítomnost základního instančního rozhraní.
    """

    # --- TECHNICKÉ ATRIBUTY (Vštěpované továrnou create_instance) ---
    __is_constant__: bool
    __is_mutable__: bool
    __mixins__: tuple[type, ...]

    # --- VEŘEJNÉ ROZHRANÍ (Garantované bází InstanceBase) ---
    @property
    def meta(self) -> "SimpleObjectMetadataProtocol":
        """Veřejný přístup k metadatům třídy vlastníka."""
        ...

    def init_mixins(self) -> None:
        """Kotva pro reaktivní inicializaci mixinových vlastností."""
        ...

    # --- VNITŘNÍ HOOKY (Garantované bází InstanceBase) ---
    def _before_update(self, new_value: Any) -> None:
        """Hook spouštěný před změnou hodnoty. Základ pro Permission mixiny."""
        ...

    # --- ČISTÉ INSTANČNÍ JÁDRO ---
    @property
    def value(self) -> Any:
        """Veřejná property pro přístup k hodnotě instance (generovaná dynamicky)."""
        ...