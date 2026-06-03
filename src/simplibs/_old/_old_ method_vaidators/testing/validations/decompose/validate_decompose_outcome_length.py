# Outers
from ......exceptions import SimpleObjectMetadataError
from ....utils import exception_context_for_classmethod

def validate_decompose_outcome_length(
    calculate_default: tuple,
    inners: tuple,
    bound_method: classmethod,
) -> None:
    """
    Validuje, že metoda _decompose vrátila správnyý počet hodnot.

    ═════════════════════════════════════════════════════════════════
    ⚠️ METHOD LOGIC ERROR: Vrácen nesprávný počet hodnot
    ═════════════════════════════════════════════════════════════════
    Expected:  {repr(inner_names_tuple)} (tuple)
    Got:       {repr(calculate_default)} (tuple)
    Problem:   Očekávaný počet položek:{len(inners)}, obdržený počet položek: {len(calculate_default)}.
    Context:   Kontrola a validace metadat pro: {class_name}.{method_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Metoda _decompose musí vracet hodnoty odpovídající prvkům z inners.
         • Upravte návratovou hodnotu '_decompose' tak, aby obsahovala přesně {expected_count} prvků.
         • Očekávané pořadí prvků: '{', '.join(inner_names_tuple)}'.
         • Příklad dle defualtních hodnot z inners:
         •     return ({', '.join(inner_values_tuple)})
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Podmínka výjimky
    if len(calculate_default) != len(inners):

        # 2. Výpočet proměnných
        _, _, context = exception_context_for_classmethod(bound_method)
        expected_count = len(inners)
        got_count = len(calculate_default)
        inner_names_tuple = (inner.meta.name_snake for inner in inners)
        inner_values_tuple = (inner.meta.default for inner in inners)

        # 3. Vyvolání výjimky
        raise SimpleObjectMetadataError(
            error_name="METHOD LOGIC ERROR",
            value_label="Vrácen nesprávný počet hodnot",
            expected=f"{repr(inner_names_tuple)} (tuple)",
            value=calculate_default,
            problem=f"Očekávaný počet položek:{expected_count}, obdržený počet položek: {got_count}.",
            context=context,
            how_to_fix=(
                "Metoda _decompose musí vracet hodnoty odpovídající prvkům z inners."
                f"Upravte návratovou hodnotu '_decompose' tak, aby obsahovala přesně {expected_count} prvků.",
                f"Očekávané pořadí prvků: '{', '.join(inner_names_tuple)}'.",
                "Příklad dle defualtních hodnot z inners:",
                f"    return ({', '.join(inner_values_tuple)})"
            ),
            exception=ValueError
        )