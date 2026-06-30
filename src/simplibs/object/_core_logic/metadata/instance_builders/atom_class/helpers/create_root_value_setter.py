from typing import Any, TYPE_CHECKING
from collections.abc import Callable
# Annotations
if TYPE_CHECKING:
    from ......protocols.metadata import SimpleMetadataLike
    from ......protocols.instance import SimpleInstanceLike


def create_root_value_setter(
    meta: "SimpleMetadataLike",
    base_class_name: str
) -> Callable:
    """
    Vytvoří reaktivní metodu _root_value_setter pro danou komponentu.
    Zajišťuje bezpečný zápis hodnoty a řízení reaktivního bublání nahoru.
    """

    def _root_value_setter(
        self: "SimpleInstanceLike",
        value: Any,
        recalculate_up: bool = True
    ) -> None:
        """Interní metoda pro zápis hodnoty s možností řízení reaktivního bublání."""

        # 1. Normalizace a validace nové hodnoty
        new_value = self.normalize(value, process_none=True)

        # 2. Kontrola, zda hodnota není shodná s aktuální
        # noinspection PyBroadException
        try:
            if self._value == new_value:
                return
        except Exception:
            pass

        # 3. Zápis hodnoty
        self._value = new_value

        # 4. Logování změny (všechny instance včetně inners)
        from simplibs.object.settings.logging import log_value_event
        log_value_event(self.__class__, new_value, event="change")

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