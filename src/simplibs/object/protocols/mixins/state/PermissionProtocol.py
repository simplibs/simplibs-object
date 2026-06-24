from typing import Protocol, runtime_checkable
# Outers
from ..base_class import SimpleMixinProtocol


@runtime_checkable
class PermissionProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protokol pro mixin Permission.

    Pracuje s atributem _lock definovaným v

    Garantuje schopnost uzamykat instanci proti změnám (Read-only režim)
    pomocí aktivace vnitřního zámku a validace skrze hook před aktualizací.
    """

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