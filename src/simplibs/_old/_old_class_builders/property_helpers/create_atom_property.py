from typing import Any
# Outers
from ....._types import SimpleMetaType


def create_atom_property(
    meta: SimpleMetaType,
) -> property:
    """
    Vytváří plnohodnotnou property (getter/setter) pro přístup k vnitřnímu slotu.
    Uzamkne název atributu do closure pro maximální čitelnost a rychlost.
    """

    # 1. Definice Getteru
    def getter(self) -> Any:
        return getattr(self, meta.name_private).value

    # 1.1 Definice anotace getteru
    getter.__annotations__ = {"return": meta.value_type}

    # 2. Definice Setteru
    def setter(self, value: Any) -> None:

        # 2.1 Normalizace a validace nové hodnoty
        new_normalized = self.normalize(value, process_none=True)

        # 2.2 Načtení staré hodnoty přímo ze slotu
        old_value = getattr(self, meta.name_private).value

        # 2.3 Zápis a spuštění update kaskády pouze při reálné změně
        if old_value != new_normalized:
            self.__setattr__(meta.name_private, new_normalized)

            # 2.3.1 Zpuštění přepočtu pro vnější prvky
            if self._owner is not None:
                self._owner._recalculate_up()

    # 2.4 Definice anotace setteru
    setter.__annotations__ = {"value": meta.value_type, "return": None}

    # 3. Definice docstringu
    doc_string = (
        f"Hodnota typu `{meta.value_type.__name__}`.\n"
        f"\n"
        f"Getter vrací normalizovanou hodnotu uloženou ve vnitřním slotu `{meta.name_snake}`.\n"
        f"Setter provádí normalizaci, validaci a případně spouští aktualizační kaskádu (`_on_update`)."
    )

    # 4. Sestavení a navrácení hotové property
    return property(
        fget=getter,
        fset=setter,
        doc=doc_string
    )