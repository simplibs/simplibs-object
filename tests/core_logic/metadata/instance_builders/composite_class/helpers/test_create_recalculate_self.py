from typing import TYPE_CHECKING
from collections.abc import Callable
# Annotations
if TYPE_CHECKING:
    from ......protocols.metadata import SimpleMetadataLike
    from ......protocols.instance.core_classes import CompositeInstanceProtocol


def create_recalculate_self(
    meta: "SimpleMetadataLike",
    base_class_name: str
) -> Callable:
    """
    Vytvoří reaktivní metodu _recalculate_up pro kompozitní bázi (CompositeBase).
    Při změně vnitřního prvku přepočítá hodnotu kompozice a bublá směrem nahoru.
    """

    def _recalculate_self(
        self: "CompositeInstanceProtocol"
    ) -> None:

        # 1. Získání slovníku s hodnotami inners
        current_values = {
            inner.meta.name_snake: getattr(self, inner.meta.name_private).value
            for inner in meta.inners
        }

        # 2. Výpočet hodnoty
        new_value = self.calculate_value(**current_values)

        # 3. Zápis a propagace pouze při reálné změně hodnoty
        # noinspection PyBroadException
        try:
            if self._value == new_value:
                return
        except Exception:
            pass

        # Uložení nové vypočítané hodnoty
        self._value = new_value

        # 4. Pokud tuto kompozici vlastní jiná nadřazená kompozice, předáme update výše
        if self._owner:
            # noinspection PyProtectedMember
            self._owner._recalculate_self()

    # Nastavení správných jmen pro debugování a introspekci
    _recalculate_self.__name__ = "_recalculate_self"
    _recalculate_self.__qualname__ = f"{base_class_name}._recalculate_self"
    _recalculate_self.__annotations__ = {"return": None}

    _recalculate_self.__doc__ = (
        f"Přepočítá hodnotu kompozice {meta.class_name} a předá požadavek na přepočet směrem nahoru v hierarchii.\n"
        f"\n"
        f"Tato metoda provádí reaktivní aktualizaci stavu. "
        f"Spustí se automaticky, jakmile dojde ke změně hodnoty některého z vnitřních prvků (atomů či sub-kompozic).\n"
    )

    return _recalculate_self