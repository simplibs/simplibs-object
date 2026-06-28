from typing import TYPE_CHECKING, Any
# Outers
from ........exceptions import SimpleMetadataError
# Annotations
if TYPE_CHECKING:
    from ........protocols.methods import ClassMethodProtocol


def validate_kwargs_defaults(
    expected_kwargs_defaults: dict[str, Any],
    bound_method: "ClassMethodProtocol",
    base_info: dict[str, str | tuple[str, ...]],
) -> None:
    """
    Validuje, že pokud uživatel v signatuře metody definoval defaultní hodnoty,
    shodují se přesně s hodnotami definovanými v '_inners'.

    V systému Simple je kompozice deterministická. Výchozí hodnoty logiky
    jsou pevně dané strukturou objektu. Uživatelská definice v metodě
    slouží pouze pro dokumentaci a podporu IDE, nesmí však měnit logiku.

    ═════════════════════════════════════════════════════════════════
    ⚠️ METHOD SIGNATURE ERROR: Nepovolená hodnota defaultního parametr
    ═════════════════════════════════════════════════════════════════
    Expected:  Hodnota '{expected_value}' (podle definice v '_inners')
    Got:       repr(value), (type)
    Problem:   Parametr '{name}' nevyhovuje očekávanému.
    Context:   Kontrola a validace metadat pro: {class_name}.{method_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Sjednoťte defaultní hodnotu parametru '{name}' s jeho definicí v '_inners'.
         • Doporučená hodnota: {repr(expected_value)}
         • Nebo defaultní hodnotu v signatuře metody zcela odstraňte;
         • systém ji do metody doplní automaticky během inicializace metadat.
         • Expected structure:
         • class {class_name}(SimpleObject):
         •     ...
         •     @classmethod
         •     def {method_name}({', '.join(expected_params)}):
         •         ...
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Načtení uživatelských defaultů z metody
    # (Hledáme v __kwdefaults__, protože naše parametry jsou Keyword-Only)
    method_kwargs_defaults = bound_method.__func__.__kwdefaults__ or {}

    # 2. Pokud uživatel žádné defaulty nenapsal, končíme (Happy Path)
    if not method_kwargs_defaults:
        return

    # 3. Iterace a kontrola shody
    for name, value in method_kwargs_defaults.items():

        # 3.1 Načtení očekávané hodnoty
        expected_value = expected_kwargs_defaults.get(name)

        # 3.2 Kontrola identity/rovnosti
        if value != expected_value:

            # 3.2.1 Příprava proměných
            excepted_structure = base_info["excepted_structure"]
            context = base_info["context"]

            # 3.2.2 Vyvolání výjimky
            raise SimpleMetadataError(
                error_name="METHOD SIGNATURE ERROR",
                value_label="Nepovolená hodnota defaultního parametru",
                expected=f"Hodnota '{expected_value}' (podle definice v '_inners')",
                value=value,
                problem=f"Parametr '{name}' nevyhovuje očekávanému.",
                context=context,
                how_to_fix=(
                    f"Sjednoťte defaultní hodnotu parametru '{name}' s jeho definicí v '_inners'.",
                    f"Doporučená hodnota: {repr(expected_value)}",
                    "Nebo defaultní hodnotu v signatuře metody zcela odstraňte;",
                    "systém ji do metody doplní automaticky během inicializace metadat.",
                ) + excepted_structure,
                exception=ValueError
            )
