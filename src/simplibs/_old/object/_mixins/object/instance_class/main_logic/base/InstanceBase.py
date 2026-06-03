from typing import Any, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ...metadata.SimpleObjectMetadata import SimpleObjectMetadata

class InstanceBase:
    """
    Základní mixin pro instanci SimpleObjectu.
    Zajišťuje přístup k vnitřnímu jádru (Core/Atom) a k jeho hodnotě.
    """

    # Očekává metadata od třídy, kde bude mixin použit
    meta: 'SimpleObjectMetadata'

    @property
    def core(self) -> Any:
        """Vrací instanci jádra (Atomu), která drží skutečnou hodnotu."""
        return getattr(self, self.meta.name_private)

    @property
    def value(self) -> Any:
        """Proxy přístup k hodnotě uložené v jádru."""
        return self.core.value

    @value.setter
    def value(self, new_value: Any) -> None:
        """Nastaví novou hodnotu do jádra a spustí on_update."""
        self.core.value = new_value
        self._on_update()

    def _on_update(self) -> None:
        """
        Hook metoda pro uživatelskou logiku po změně hodnoty.
        K přepsání v potomcích.
        """
        ...

    # def on_update(self) -> Any:
    #     """Veřejné rozhraní pro spuštění aktualizační logiky."""
    #     return self._on_update()