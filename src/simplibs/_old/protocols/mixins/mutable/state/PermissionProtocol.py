from typing import Protocol, runtime_checkable
# Outers
from ....types import SimpleInstanceType


@runtime_checkable
class PermissionProtocol(SimpleInstanceType, Protocol):
    """
    Protokol pro mixin Permission.

    Garantuje schopnost uzamykat instanci proti změnám (Read-only režim)
    pomocí aktivace vnitřního zámku a validace skrze hook před aktualizací.
    """

    # --- TECHNICKÉ ATRIBUTY (Inicializované v init_mixins) ---
    _locked: bool

    # --- ERGONOMICKÉ PROPERTIES ---

    @property
    def is_locked(self) -> bool:
        """Vrací True, pokud je instance aktuálně uzamčena pro zápis."""
        ...

    # --- VEŘEJNÉ API PRO SPRÁVU ZÁMKU ---

    def lock(self) -> None:
        """Uzamkne instanci. Jakýkoliv pokus o změnu hodnoty vyvolá ValueError."""
        ...

    def unlock(self) -> None:
        """Odemkne instanci a povolí opětovný zápis a změny hodnoty."""
        ...