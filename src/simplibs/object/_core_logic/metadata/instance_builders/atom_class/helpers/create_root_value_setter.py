from typing import Any, Callable
# Outers
from .....protocols import SimpleMetadataType


def create_root_value_setter(
    meta: SimpleMetadataType,
    base_class_name: str
) -> Callable:
    """
    Vytvoří reaktivní metodu _root_value_setter pro danou komponentu.
    Zajišťuje bezpečný zápis hodnoty a řízení reaktivního bublání nahoru.
    """

    def _root_value_setter(
        self,
        value: Any,
        recalculate_up: bool = True
    ) -> None:
        """Interní metoda pro zápis hodnoty s možností řízení reaktivního bublání."""

        # 1. Normalizace a validace nové hodnoty
        new_value = self.normalize(value, process_none=True)

        # 2. Kontrola, zda hodnota není shodná s aktuální
        try:
            if self._value == new_value:
                return
        except Exception:
            pass

        # 3. Zápis hodnoty
        self._value = new_value

        # 4. Spuštění přepočtu pro vnější prvky
        if self._owner and recalculate_up:
            # noinspection PyProtectedMember
            self._owner._recalculate_self()

    # Nastavení správných jmen pro debugování a introspekci
    _root_value_setter.__name__ = "_root_value_setter"
    _root_value_setter.__qualname__ = f"{base_class_name}._root_value_setter"
    _root_value_setter.__annotations__ = {"value": Any, "recalculate_up": bool, "return": None}

    _root_value_setter.__doc__ = (
        f"Zabezpečuje zápis hodnoty do instance {meta.class_name}.\n"
        f"\n"
        f"Provede normalizaci, porovná hodnotu vůči stávající a v případě změny\n"
        f"může aktivovat reaktivní přepočet vlastníka (bublání nahoru).\n"
    )

    return _root_value_setter