# Outers
from .....exceptions import SimpleObjectMetadataError
from ..utils import exception_context_for_classmethod
# Inners
from .utils import convert_annotation_to_type_set



def validate_bound_method_annotations(
    bound_method_annotations: dict[str, type],
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
         • Nebo defaultní anotaci v signatuře metody zcela odstraňte;
         • systém ji do metody doplní automaticky během inicializace metadat.
         • Example:
         • class {class_name}(SimpleObject):
         •     ...
         •     @classmethod
         •     def {method_name}(cls, ..., param: {expected_names}) -> {return_name}:
         •         ...
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Načtení uživatelských anotací z metody
    method_annotations = bound_method.__func__.__annotations__ or {}

    # 2. Pokud uživatel žádné anotace nenapsal, končíme (Happy Path)
    if not method_annotations:
        return

    # 2. Validace
    if method_annotations:

        # 2.1 Cyklus skrze uvedené anotace
        for name, annotation in method_annotations.items():

            # 2.2 Načtení očekávané anotace
            # (převod na sets, kuli UnionType)
            expected_type = bound_method_annotations.get(name)
            expected_type_set = convert_annotation_to_type_set(expected_type)
            annotation_set = convert_annotation_to_type_set(annotation)

            # 2.3 Kontrola zda anotace je uvedena v očekávaném
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
                        "Nebo anotaci v signatuře metody zcela odstraňte;",
                        "systém ji do metody doplní automaticky během inicializace metadat.",
                        "Example:",
                        f"class {class_name}(SimpleObject):",
                        "    ...",
                        "    @classmethod",
                        f"    def {method_name}(cls, ..., param: {expected_names}):",
                        "        ..."
                    ),
                    exception=TypeError
                )
