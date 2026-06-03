from typing import Any
from simplibs.sentinels import UNSET
# Outers
from ....._types import SimpleMetaType


def create_composite_property(
    meta: SimpleMetaType,
) -> property:
    """
    Vytváří plnohodnotnou property (getter/setter) pro přístup ke kompozitní hodnotě.
    Getter vrací hodnotu kompozice (self.<private>.value).
    Setter je povolen pouze pokud kompozice definuje decompose_value.
    """

    # 1. Getter
    def getter(self) -> Any:
        return getattr(self, meta.name_private).value

    # 1.1 Definice anotace getteru
    getter.__annotations__ = {"return": meta.value_type}

    # 2. Setter
    def setter(self, value: Any) -> None:

        # 2.1 Ověření, zda kompozice podporuje dekompozici
        if not self.meta.is_decomposeable:
            raise TypeError(
                f"Kompozice '{meta.class_name}' nepodporuje přiřazení hodnoty, "
                f"protože nemá definovanou metodu decompose_value()."
            )

        # 2.2 Validace a normalizace nové hodnoty
        normalized_value = self.normalize(value, process_none=True)

        # 2.3 Rozložení hodnoty
        values = self.decompose_value(normalized_value)

        # 2.4 Zapsání hodnot do vnitřních prvků
        for inner, value in zip(self.meta.inners, values):
            setattr(self, inner.meta.name_snake, value)

        # 2.5 Zápis pouze při změně
        if self._value != normalized_value:
            self._value = normalized_value

            # 2.5.1 Zpuštění přepočtu pro vnější prvky
            if self._owner is not None:
                self._owner._recalculate_up()

    # 2.6 Definice anotace setteru
    setter.__annotations__ = {"value": meta.value_type, "return": None}

    # 3. Docstring
    doc_string = (
        f"Hodnota typu `{meta.value_type.__name__}`.\n"
        f"\n"
        f"Getter vrací hodnotu kompozice uloženou ve vnitřním slotu `{meta.name_private}`.\n"
        f"Setter je povolen pouze pokud kompozice definuje `decompose_value`, jinak vyvolá chybu."
    )

    # 4. Sestavení property
    return property(
        fget=getter,
        fset=setter,
        doc=doc_string
    )
