from typing import Protocol, Any, runtime_checkable, TYPE_CHECKING
# Outers
from ..methods import LogicSignature, P, R
# Inners
from .SimpleConstantProtocol import SimpleConstantProtocol
# Annotations
if TYPE_CHECKING:
    from ..metadata import SimpleObjectMetadataProtocol
    from ..types import SimpleClassType


@runtime_checkable
class SimpleObjectProtocol(SimpleConstantProtocol, Protocol):
    """
    Protokol pro SimpleObject. Reprezentuje plné rozhraní kompozitních tříd (Nodes),
    včetně vnitřních prvků, transformační logiky a pokročilého dynamického typování.
    """

    # --- KOVARIANTNÍ PŘEPIS METADAT (Upřesňujeme na kompozitní metadata) ---
    __metadata__: "SimpleObjectMetadataProtocol"

    @property
    def meta(self) -> "SimpleObjectMetadataProtocol":
        """Veřejný přístup k nejvyšší úrovni kompozitních metadat třídy."""
        ...

    # --- VNITŘNÍ ROZHRANÍ (Definuje uživatel při zakládání kompozice) ---
    _inners: tuple["SimpleClassType", ...]

    @classmethod
    def _logic(cls, *args: P.args, **kwargs: P.kwargs) -> R:
        """Povinná výpočetní metoda pro kompozici, která určuje její signaturu."""
        ...

    @classmethod
    def _decompose(cls, value: Any) -> Any:
        """Nepovinná metoda pro rozklad hlavní hodnoty."""
        ...

    # --- VNĚJŠÍ ROZHRANÍ (Metody přidané/dostupné pro práci s kompozicí) ---
    @classmethod
    def calculate_value(cls: LogicSignature[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
        """
        Dynamicky spočítá hodnotu kompozice a díky ParamSpec
        propisuje konkrétní parametry z uživatelské metody '_logic'.
        """
        ...

    @classmethod
    def decompose_value(cls, value: Any) -> Any:
        """Rozloží hlavní hodnotu na vnitřní komponenty."""
        ...