# Outers
from ........exceptions import SimpleMetadataError


def validate_method_param_match_expected(
    method_params: tuple[str, ...],
    expected_params: tuple[str, ...],
    base_info: dict[str, str | tuple[str, ...]],
) -> None:
    """
    Validuje, že názvy parametrů metody přesně odpovídají očekávání.

    ═════════════════════════════════════════════════════════════════
    ⚠️ METHOD SIGNATURE ERROR: Neshoda parametrů
    ═════════════════════════════════════════════════════════════════
    Expected:  {repr(expected_params)} (tuple)
    Got:       {repr(method_params)} ({type(method_params).__name__})
    Problem:   Zadané parametry neodpovídají očekávanému.
    Context:   Kontrola a validace metadat pro: {class_name}.{method_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Upravte definici metody tak, aby parametry odpovídaly očekávanému.
         • Prvním parametrem musí být vždy 'cls'.
         • Názvy dalších parametrů musí přesně odpovídat snake_case názvům vašich '_inners'.
         • Expected structure:
         • class {class_name}(SimpleObject):
         •     ...
         •     @classmethod
         •     def {method_name}({', '.join(expected_params)}):
         •         ...
    ═════════════════════════════════════════════════════════════════
    """
    # 1. Podmínka výjimky
    if method_params != expected_params:

        # 2. Vypočet proměných
        excepted_structure = base_info["excepted_structure"]
        context = base_info["context"]

        # 3. Vyvolání výjimky
        raise SimpleMetadataError(
            error_name="METHOD SIGNATURE ERROR",
            value_label=f"Neshoda parametrů",
            expected=f"{repr(expected_params)} (tuple)",
            value=method_params,
            problem="Zadané parametry neodpovídají očekávanému.",
            context=context,
            how_to_fix=(
                f"Upravte definici metody tak, aby parametry odpovídaly očekávanému.",
                "Prvním parametrem musí být vždy 'cls'.",
                "Názvy dalších parametrů musí přesně odpovídat snake_case názvům vašich '_inners'.",
            ) + excepted_structure,
            exception=TypeError
        )