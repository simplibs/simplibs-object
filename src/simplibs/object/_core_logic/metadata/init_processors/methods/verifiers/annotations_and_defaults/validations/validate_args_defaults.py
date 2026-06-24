from typing import Any
# Outers
from .......protocols import ClassMethodProtocol
from .......exceptions import SimpleMetadataError


def validate_args_defaults(
    expected_args_defaults: tuple[Any, ...],
    expected_params: tuple[str, ...],
    bound_method: ClassMethodProtocol,
    base_info: dict[str, str | tuple[str, ...]],
) -> None:
    """
    Validuje, že defaultní hodnoty pozičních parametrů odpovídají
    defaultům definovaným v '_inners'.

    V systému Simple jsou defaulty deterministické a odvozené z metadat.
    Uživatel je nesmí měnit – může je pouze vynechat.

    ═════════════════════════════════════════════════════════════════
    ⚠️ METHOD SIGNATURE ERROR: Nepovolená defaultní hodnota
    ═════════════════════════════════════════════════════════════════
    Expected:  Žádná hodnota a nebo hodnota dle definice v '_inners': '{expected_value}'
    Got:       {repr(method_params)} ({type(method_params).__name__})
    Problem:   Parametr '{param_name}' má nesprávnou defaultní hodnotu.
    Context:   Kontrola a validace metadat pro: {class_name}.{method_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Sjednoťte defaultní hodnotu parametru '{param_name}' s jeho definicí v '_inners'.
         • Doporučená hodnota: {repr(expected_value)}
         • Nebo defaultní hodnotu v signatuře metody zcela odstraňte;
         • systém ji doplní automaticky během inicializace metadat.
         • Expected structure:
         • class {class_name}(SimpleObject):
         •     ...
         •     @classmethod
         •     def {method_name}({', '.join(expected_params)}):
         •         ...
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Načtení uživatelských defaultů
    method_args_defaults = bound_method.__func__.__defaults__ or ()

    # 2. Pokud uživatel žádné defaulty nenapsal → OK
    if not method_args_defaults:
        return

    # 3. Kontrola shody hodnot
    for index, (value, expected_value) in enumerate(zip(method_args_defaults, expected_args_defaults)):
        if value != expected_value:

            # 2. Vypočet proměných
            excepted_structure = base_info["excepted_structure"]
            context = base_info["context"]
            param_name = expected_params[index]

            raise SimpleMetadataError(
                error_name="METHOD SIGNATURE ERROR",
                value_label=f"Nepovolená defaultní hodnota",
                expected=f"Žádná hodnota a nebo hodnota dle definice v '_inners': '{expected_value}'",
                value=value,
                problem=f"Parametr '{param_name}' má nesprávnou defaultní hodnotu.",
                context=context,
                how_to_fix=(
                    f"Sjednoťte defaultní hodnotu parametru '{param_name}' s jeho definicí v '_inners'.",
                    f"Doporučená hodnota: {repr(expected_value)}",
                    "Nebo defaultní hodnotu v signatuře metody zcela odstraňte;",
                    "systém ji doplní automaticky během inicializace metadat.",
                ) + excepted_structure,
                exception=ValueError
            )
