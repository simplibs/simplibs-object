from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
from .._exceptions_helpers import exception_info_for_inners
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def validate_inner_is_not_simple_class(
    inner: "SimpleClassLike",
    owner_class: "SimpleClassLike"
) -> None:
    """
    Validuje, že vnitřní prvek není přímo základní třída SimpleObject nebo SimpleConstant.

    Tato kontrola brání logické chybě, kdy by byla do kompozice vložena
    abstraktní základní třída namísto konkrétního potomka s definovanými daty.

    ═════════════════════════════════════════════════════════════════
    ⚠️ INVALID INNERS DEFINITION: Prvek z _inners je abstraktní základ
    ═════════════════════════════════════════════════════════════════
    Expected:  Konkrétní potomek třídy SimpleObject nebo SimpleConstant.
    Got:       repr(inner) (type)
    Problem:   V definici '_inners' třídy '{class_name}' je přímo třída '{inner.__name__}'..
    Context:   Kontrola a validace metadat pro: {class_name}.{attribute_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Vnitřní prvky atributu _inners mohou být pouze potomci třídy SimpleObject a SimpleConstant.
         • Vnitřním prvkem ale nemůže být přímo třída SimpleObject nebo SimpleConstant.
         • Základní třídy (SimpleObject, SimpleConstant) slouží pouze jako vzory pro dědění.
         • Nahraďte tento prvek jeho konkrétním potomkem, který reprezentuje reálná data.
         • Acceptable definitions:
         • class {class_name}(class_parrent):
         •     _inners: tuple = (PrvekA, PrvekB)
         •     ...
    ═════════════════════════════════════════════════════════════════
    """

    # Vnitřní import předcházející cilkulární chybě
    from .......SimpleConstant import SimpleConstant
    from .......SimpleObject import SimpleObject

    # 1. Podmínka výjimky
    if inner is SimpleConstant or inner is SimpleObject:

        # 2. Vypočet proměných
        (class_name,
         error_name,
         context,
         acceptable_definitions
         ) = exception_info_for_inners(owner_class)

        # 3. Vyovlání výjimky
        raise SimpleMetadataError(
            error_name=error_name,
            value_label="Prvek z _inners je abstraktní základ",
            expected="Konkrétní potomek třídy SimpleObject nebo SimpleConstant.",
            value=inner,
            problem=f"V definici '_inners' třídy '{class_name}' je přímo třída '{inner.__name__}'.",
            context=context,
            how_to_fix=(
                "Vnitřní prvky atributu _inners mohou být pouze potomci třídy SimpleObject a SimpleConstant.",
                "Vnitřním prvkem ale nemůže být přímo třída SimpleObject nebo SimpleConstant.",
                "Základní třídy (SimpleObject, SimpleConstant) slouží pouze jako vzory pro dědění.",
                "Nahraďte tento prvek jeho konkrétním potomkem, který reprezentuje reálná data.",
            ) + acceptable_definitions,
            exception=TypeError
        )


_DESIGN_NOTES = """
# validate_inner_is_not_simple_object_class

## Účel
Tato validace funguje jako doplňkový filtr k `validate_inner_is_simple_object_subclass`. 
Zatímco předchozí krok ověřil příslušnost k "rodině", tento krok hlídá, aby 
v rodokmenu nefiguroval přímo "Praotec" (základní třída).

## Proč je tato kontrola separovaná?
1. **Sémantický rozdíl**: Být "podtřídou" je technický požadavek na kompatibilitu. 
   Nebýt "přímo tou třídou" je logický požadavek na smysluplnost dat.
2. **Čistota signatur**: Pokud by do pipeline prošel přímo `SimpleObject`, 
   následné procesory (např. `create_names`) by generovaly nesmyslné názvy 
   jako `simple_object` v argumentech metody `_logic`, což by vedlo k 
   nepřehlednému a nefunkčnímu kódu.

## Technické provedení
Používáme operátor `is`, který v Pythonu porovnává identitu objektů v paměti. 
Je to nejrychlejší a nejpřesnější způsob, jak ověřit, zda dvě reference 
ukazují na naprosto stejnou třídu. Reference na `simple_object_base` je 
opět předávána z řídící metody, aby byla zachována konzistence v rámci 
celého validačního cyklu.
"""