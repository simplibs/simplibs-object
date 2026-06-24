from typing import Protocol, Any, runtime_checkable, TYPE_CHECKING
# Inners
from .SimpleBaseProtocol import SimpleBaseProtocol


@runtime_checkable
class SimpleConstantProtocol(
    SimpleBaseProtocol,
    Protocol
):
    """
    Protokol pro SimpleConstant. Reprezentuje rozhraní konstantních tříd (Atomů),
    včetně uživatelsky definovaných chráněných atributů a veřejných validačních metod.
    """

    # --- VNITŘNÍ ROZHRANÍ (Definuje uživatel při zakládání třídy) ---
    _type: type
    _default: Any

    @classmethod
    def _validate(cls, value: Any, *, return_bool: bool = False) -> bool | Exception:
        """Nepovinná doplňková validace definovaná uživatelem."""
        ...

    # --- VNĚJŠÍ ROZHRANÍ (Metody přidané/dostupné pro práci s konstantou) ---
    @classmethod
    def validate_type(cls, value: Any, *, return_bool: bool = False) -> bool:
        """Provede deterministickou validaci typu na základě metadat třídy."""
        ...

    @classmethod
    def validate(cls, value: Any, *, return_bool: bool = False) -> bool:
        """Provede validaci typu a validaci skrze upřesňující validační metodu."""
        ...

    @classmethod
    def is_valid(cls, value: Any) -> bool:
        """Vrátí True, pokud hodnota projde kompletní validací, jinak False."""
        ...

    @classmethod
    def normalize(cls, value: Any, *, process_none: bool = False) -> Any:
        """Normalizuje hodnotu. Vrací hodnotu nebo vyvolá SimpleLogicError."""
        ...

    @classmethod
    def bool_or_raise_validate_error(
        cls, value: Any, problem: str, *, return_bool: bool = False
    ) -> bool:
        """Pomocná metoda pro použití uvnitř uživatelských '_validate'."""
        ...