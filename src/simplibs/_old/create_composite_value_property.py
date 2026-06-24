from typing import Any
# Outers
from .....protocols import SimpleMetadataType
from ....._utils.properties.helpers.validations import raise_class_not_decomposeable


def create_composite_value_property(
    meta: SimpleMetadataType
) -> property:
    """
    Vytváří property (getter/setter) pro hlavní 'value' kompozitního objektu.
    Umožňuje shora-dolů rozklad (dekompozici) hodnoty do vnitřních prvků.
    """

    # 1. Definice Getteru
    def getter(self) -> Any:
        return self._value

    # 2. Definice anotace getteru
    getter.__annotations__ = {"return": meta.value_type}

    # 3. Definice Setteru
    def setter(self, value: Any) -> None:

        # 3.1 Ověření, zda tato kompozice podporuje dekompozici
        if not meta.is_decomposeable:
            raise_class_not_decomposeable(meta)

        # 3.2 Zápis hodnoty a aktivace přepočtu ownera
        self._root_value_setter(value, recalculate_up=True)

        # 3.3 Rozložení hodnoty a zápis do vnitřních prvků
        self._recalculate_inners()

        # 3.4 Případné logování (je-li nastaveno)
        self._log_outcome(value)

    # 4. Definice anotace setteru
    setter.__annotations__ = {"value": meta.value_type, "return": None}

    # 5. Definice docstringu
    doc_string = (
        f"Kompozitní hodnota typu `{meta.value_type_name}`.\n"
        f"\n"
        f"Getter vrací aktuální vypočítanou hodnotu kompozice.\n"
        f"Setter rozloží (dekomponuje) vstupní hodnotu a distribuuje ji do vnitřních prvků."
    )

    # 6. Sestavení a navrácení hotové property
    return property(
        fget=getter,
        fset=setter,
        doc=doc_string
    )