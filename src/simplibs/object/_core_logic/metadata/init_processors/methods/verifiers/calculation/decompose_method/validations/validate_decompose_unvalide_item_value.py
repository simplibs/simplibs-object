from typing import Any, TYPE_CHECKING
# Outers
from .........exceptions import SimpleMetadataError
from ...._exceptions_helpers import exception_context_for_classmethod
# Annotations
if TYPE_CHECKING:
    from .........protocols.methods import ClassMethodProtocol
    from .........protocols.classes import SimpleClassLike


def validate_decompose_unvalide_item_value(
    value: Any,
    inner: "SimpleClassLike",
    inners: tuple["SimpleClassLike", ...],
    bound_method: "ClassMethodProtocol",
) -> None:
    """
    Vytváří výjimku, když metoda _decompose vrátila prvek,
    který sice odpovídá typu, ale neodpovídá defaultní hodnotě inneru.

    ═════════════════════════════════════════════════════════════════
    ⚠️ METHOD LOGIC ERROR: Neplatná hodnota prvku z návratové hodnoty
    ═════════════════════════════════════════════════════════════════
    Expected:  Hodnota '{inner.meta.default!r}' (podle definice v '{inner.meta.owner_class.__name__}').
    Got:       {repr(value)} ({type(value).__name__})
    Problem:   Prvek '{inner.meta.name_snake}' neodpovídá defaultní hodnotě definované v '_inners'.
    Context:   Kontrola a validace metadat pro: {class_name}.{method_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Upravte výpočet v metodě '_decompose' tak, aby vracel defaultní hodnotu.
         • Očekávaná hodnota je '{inner.meta.default!r}'.
         • Ujistěte se, že pořadí prvků v returnu odpovídá pořadí v '_inners'.
         • Očekávané pořadí prvků: '{', '.join(inner_names_tuple)}'.
         • Příklad dle defualtních hodnot z inners:
         •     return ({', '.join(inner_values_tuple)})
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Podmínka výjimky
    if value != inner.meta.default:

        # 2. Výpočet proměnných
        class_name, method_name, context = exception_context_for_classmethod(bound_method)
        meta = inner.meta
        inner_values = tuple(inner.meta.default for inner in inners)

        # 3. Vyvolání výjimky
        raise SimpleMetadataError(
            error_name="METHOD LOGIC ERROR",
            value_label="Neplatná hodnota prvku z návratové hodnoty",
            expected=f"Hodnota '{meta.default!r}' (podle definice v '{meta.class_name}').",
            value=value,
            problem=f"Prvek '{meta.name_snake}' neodpovídá defaultní hodnotě definované v '_inners'.",
            context=context,
            how_to_fix=(
                f"Zkontrolujte výpočet prvku '{meta.name_snake}' v metodě '_decompose'.",
                f"Očekávaná hodnota je '{meta.default!r}', ale obdrželi jsme '{value!r}'.",
                "Ujistěte se, že pořadí prvků v returnu odpovídá pořadí v '_inners'.",
                f"Očekávané pořadí prvků: '{', '.join(meta.inners_params_name)}'.",
                "Příklad dle defualtních hodnot z inners:",
                f"    return ({', '.join(map(repr, inner_values))})"
            ),
            exception=ValueError
        )
