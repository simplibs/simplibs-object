# Outers
from .....exceptions import SimpleObjectMetadataError
from ...utils import exception_context_for_classmethod


def validate_method_annotation_is_valid_type(
    annotation_set: set[type],
    expected_type_set: set[type],
    bound_method: classmethod,
) -> None:
    """
    Validuje, že anotace parametru nebo návratové hodnoty metody
    odpovídá očekávanému typu (nebo jeho podmnožině).

    ═════════════════════════════════════════════════════════════════
    ⚠️ METHOD SIGNATURE ERROR: Neplatná anotace typu
    ═════════════════════════════════════════════════════════════════
    Expected:  Anotace typu '{expected_names}'.
    Problem:   "Definovaná anotace '{annotation_names}' nevyhovuje očekávanému..
    Context:   Kontrola a validace metadat pro: {class_name}.{method_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Upravte anotaci v definici metody tak, aby odpovídala '{expected_names}'.
         • Anotace musí být stejného typu nebo jeho validní podtyp (subset).
         • Example:
         • class {class_name}(SimpleObject):
         •     ...
         •     @classmethod
         •     def {method_name}(cls, ..., param: {expected_names}) -> {return_name}:
         •         ...
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Podmínka výjimky
    if not annotation_set.issubset(expected_type_set):

        # 2. Výpočet proměnných
        class_name, method_name, context = exception_context_for_classmethod(bound_method)
        expected_names = " | ".join(t.__name__ for t in expected_type_set)
        annotation_names = " | ".join(t.__name__ for t in annotation_set)

        # 3. Vyvolání výjimky
        raise SimpleObjectMetadataError(
            error_name="METHOD SIGNATURE ERROR",
            value_label="Neplatná anotace typu",
            expected=f"Anotace typu '{expected_names}'.",
            problem=f"Definovaná anotace '{annotation_names}' nevyhovuje očekávanému.",
            context=context,
            how_to_fix=(
                f"Upravte anotaci v definici metody tak, aby odpovídala '{expected_names}'.",
                "Anotace musí být stejného typu nebo jeho validní podtyp.",
                "Example:",
                f"class {class_name}(SimpleObject):",
                "    ...",
                "    @classmethod",
                f"    def {method_name}(cls, ..., param: {expected_names}):",
                "        ..."
            ),
            exception=TypeError
        )