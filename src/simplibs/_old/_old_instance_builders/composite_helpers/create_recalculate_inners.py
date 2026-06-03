from typing import Callable
# Outers
from ...._types import SimpleMetaType


def create_recalculate_inners(
    meta: SimpleMetaType,
    base_class_name: str
)-> Callable:
    """
    Vytvoří reaktivní metodu _recalculate_up pro kompozitní bázi (CompositeBase).
    Při změně vnitřního prvku přepočítá hodnotu kompozice a bublá směrem nahoru.
    """

    def _recalculate_inners(self) -> None:

        # 1. Rozložení hodnoty na hodnoty inners
        decomposed_values = self.decompose_value(self._value)

        # 2 Distribuce hodnot do inners
        for inner, inner_value in zip(meta.inners, decomposed_values):

            # 2.1 Načtení instance inneru
            inner_instance = getattr(self, inner.meta.name_private)

            # 2.2 Zápis nové hodnoty s potlačenou propagací nahoru
            # noinspection PyProtectedMember
            inner_instance._root_value_setter(inner_value, recalculate_up=False)

            # 2.3 Pokud je prvek kompozice - aktivace přepočtu jejích vnitřních prvků
            if not inner.meta.is_constant:
                # noinspection PyProtectedMember
                inner_instance._recalculate_inners()


    # Nastavení správných jmen pro debugování a introspekci
    _recalculate_inners.__name__ = "_recalculate_inners"
    _recalculate_inners.__qualname__ = f"{base_class_name}._recalculate_inners"
    _recalculate_inners.__annotations__ = {"return": None}

    _recalculate_inners.__doc__ = (
        f"Rozloží hodnotu kompozice {meta.class_name} a předá jejich hodnoty do vlastních inners.\n"
        f"\n"
        f"Tato metoda provádí reaktivní aktualizaci stavu pro vnitřní prvky. "
        f"Spustí se automaticky, jakmile dojde ke změně hlavní hodnoty.\n"
    )

    return _recalculate_inners