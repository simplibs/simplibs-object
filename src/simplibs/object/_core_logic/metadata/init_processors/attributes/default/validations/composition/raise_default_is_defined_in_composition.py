from typing import Any
# Outers
from .......exceptions import SimpleMetadataError
from .......protocols import SimpleClassType
from .._exceptions_helpers import exception_info_for_default


def raise_default_is_defined_in_composition(
    owner_class: SimpleClassType
) -> None:
    """
    Vyvolá výjimku, pokud je u kompozice (SimpleObject) definován atribut '_default'.

    U kompozic je výchozí hodnota striktně deterministická a je vypočítána
    výhradně z výchozích hodnot vnitřních prvků (_inners) pomocí metody '_logic'.
    Manuální definice '_default' by narušila integritu tohoto výpočtu.

    ═════════════════════════════════════════════════════════════════
    ⚠️ INVALID COMPOSITION DEFINITION: Atribut '_default' není povolen
    ═════════════════════════════════════════════════════════════════
    Expected:  Kompozice bez explicitně definovaného atributu '_default'.
    Problem:   Na třídě byl nalezen atribut '_default', který u kompozic
               není přípustný.
    Context:   Kontrola a validace metadat pro: {class_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Odstraňte atribut '_default' z definice třídy {class_name}.
         • Pokud potřebujete změnit výchozí stav kompozice, upravte
           výchozí hodnoty v definicích vnořených prvků (_inners).
         • Pokud má být tato třída listem (konstantou) s vlastní
           hodnotou, odstraňte atribut '_inners' a metodu '_logic'.
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Výpočet proměnných pro výjimku
    (class_name,
     class_parent,
     error_name,
     context,
     ) = exception_info_for_default(owner_class)

    # 2. Vyvolání výjimky
    raise SimpleMetadataError(
        error_name=error_name,
        value_label="Atribut '_default' je u kompozice zakázán",
        expected="Výchozí hodnota kompozice musí být vypočtena dynamicky z vnitřních prvků.",
        problem=f"Třída '{class_name}' definuje '_default', což u objektů s '_inners' není dovoleno.",
        context=context,
        how_to_fix=(
            f"Odstraňte atribut '_default' z definice třídy '{class_name}'.",
            "Výchozí hodnotu ovlivňujte skrze výchozí hodnoty prvků v '_inners'.",
            "Ujistěte se, že správně rozlišujete mezi SimpleConstant a SimpleObject."
        ),
        exception=TypeError
    )