from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from ...._metadata.SimpleObjectMetadata import SimpleObjectMetadata


class UpdateValue:

    meta: 'SimpleObjectMetadata'
    decompose_value: Any
    create_value: Any


    @classmethod
    def update_value(cls, value: Any, **kwargs) -> Any:
        """
        Aktualizuje existující hodnotu pomocí nových parametrů.
        Vezme stávající hodnotu, rozloží ji, aktualizuje změněnými parametry
        a znovu složí do nové hodnoty.
        """
        # 1. Získáme aktuální stav rozkladem
        # decompose_value už v sobě má ošetření chyb, takže tady jen delegujeme
        current_state = cls.decompose_value(value)

        # 2. Aktualizujeme stav pomocí nových parametrů
        current_state.update(kwargs)

        # 3. Složíme novou hodnotu
        return cls.create_value(**current_state)