from typing import Any
# Outers
from ........protocols import ClassMethodProtocol, SimpleClassType
from ........exceptions import SimpleMetadataError
from ...._exceptions_helpers import exception_context_for_classmethod


def validate_decompose_unvalide_item_type(
    value: Any,
    expected_type: type,
    inner: SimpleClassType,
    inners: tuple[SimpleClassType, ...],
    bound_method: ClassMethodProtocol,
) -> None:
    """
    Vytváří výjimku, když metoda _decompose vrátila prvky nevhodného typu.

    ═════════════════════════════════════════════════════════════════
    ⚠️ METHOD LOGIC ERROR: Neplatný typu prvku z návratové hodnoty
    ═════════════════════════════════════════════════════════════════
    Expected:  Hodnota typu '{expected_type.__name__}'.' (podle definice v '{inner_metadata.owner_class.__name__}').
    Got:       {repr(value)} ({type(value).__name__})
    Problem:   Prvek '{inner_name}' není kompatibilní s definicí v '_inners'.
    Context:   Kontrola a validace metadat pro: {class_name}.{method_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Upravte anotaci v definici metody tak, aby odpovídala '{expected_names}'.
         • Anotace musí být stejného typu nebo jeho validní podtyp (subset).
         • Ujistěte se, že pořadí prvků v returnu odpovídá pořadí v '_inners'.
         • Očekávané pořadí prvků: '{', '.join(inner_names_tuple)}'.
         • Příklad dle defualtních hodnot z inners:
         •     return ({', '.join(inner_values_tuple)})
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Podmínka výjimky
    if not isinstance(value, expected_type):

        # 2. Výpočet proměnných
        class_name, method_name, context = exception_context_for_classmethod(bound_method)
        meta = inner.meta
        inner_values = (inner.meta.default for inner in inners)

        # 3. Vyvolání výjimky
        raise SimpleMetadataError(
            error_name="METHOD LOGIC ERROR",
            value_label=f"Neplatný typu prvku z návratové hodnoty",
            expected=f"Hodnota typu '{expected_type.__name__}'.' (podle definice v '{meta.class_name}').",
            value=value,
            problem=f"Prvek '{meta.name_snake}' není kompatibilní s definicí v '_inners'.",
            context=context,
            how_to_fix=(
                f"Zkontrolujte výpočet prvku '{meta.name_snake}' v metodě '_decompose'.",
                f"Očekávaný typ je '{expected_type.__name__}', ale obdrželi jsme '{type(value).__name__}'.",
                "Ujistěte se, že pořadí prvků v returnu odpovídá pořadí v '_inners'.",
                f"Očekávané pořadí prvků: '{', '.join(meta.inners_params_name)}'.",
                "Příklad dle defualtních hodnot z inners:",
                f"    return ({', '.join(inner_values)})"
            ),
            exception=TypeError
        )