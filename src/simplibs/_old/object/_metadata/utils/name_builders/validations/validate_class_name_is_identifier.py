# Outers
from ....exceptions import SimpleObjectMetadataError


def validate_class_name_is_identifier(class_name: str) -> None:
    """
    Validuje, že jméno třídy je platným identifikátorem Pythonu.

    Určeno pro zachycení nekorektních názvů u dynamicky tvořených tříd přes type(),
    které by jinak neprošly standardním parserem při statickém zápisu.

    ═════════════════════════════════════════════════════════════════
    ⚠️ CLASS NAME NOT IDENTIFIER: Invalid Python name
    ═════════════════════════════════════════════════════════════════
    Expected:  Název začínající písmenem, obsahující pouze alfanumerické znaky.
    Got:       {repr(value)} (str)
    Problem:   Název třídy '{class_name}' není platným identifikátorem.
    Context:   Strukturální kontrola jména dynamické třídy.
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Ujistěte se, že název neobsahuje mezery, pomlčky nebo tečky.
         • Název nesmí začínat číslicí.
         • Při dynamické tvorbě přes type(name, ...) zkontrolujte parametr 'name'.
    ═════════════════════════════════════════════════════════════════
    """

    if not class_name.isidentifier():
        raise SimpleObjectMetadataError(
            error_name="CLASS NAME NOT IDENTIFIER",
            value_label="class_name",
            value=class_name,
            problem=f"Název třídy '{class_name}' není platným identifikátorem.",
            expected="Název začínající písmenem, obsahující pouze alfanumerické znaky.",
            how_to_fix=(
                "Ujistěte se, že název neobsahuje mezery, pomlčky nebo tečky.",
                "Název nesmí začínat číslicí.",
                "Při dynamické tvorbě přes type(name, ...) zkontrolujte parametr 'name'."
            ),
            context="Strukturální kontrola jména dynamické třídy",
            exception=ValueError
        )


_DESIGN_NOTES = """
# validate_class_name_is_identifier

## Účel
Tato validace je "technickým filtrem" pro jména tříd. Jejím hlavním úkolem je zajistit, 
že jméno třídy splňuje syntaktická pravidla Pythonu pro identifikátory. 

## Proč je tato validace nutná (Dynamický kontext)
I když statický zápis `class MyClass:` hlídá parser Pythonu, dynamická tvorba pomocí 
`type("Název", ...)` je benevolentnější. Dovolí vytvořit třídu se jménem, které 
obsahuje mezery, pomlčky nebo začíná číslem. 

Tato funkce garantuje, že i dynamicky vytvořená třída bude mít jméno, které:
1. Nezačíná číslicí.
2. Neobsahuje mezery, pomlčky, tečky ani jiné zakázané symboly.
3. Je technicky použitelné pro další generování atributů a kódu.

## Pozice v řetězci validací
V rámci inicializace metadat tato kontrola předchází ostatním, protože definuje 
základní strukturu. Celý proces tvoří tyto tři pilíře:

1. **validate_class_name_is_identifier** (Tato funkce):
   Eliminuje mezery, pomlčky a čísla na začátku. 
   Povoluje: `[a-zA-Z0-9_]` (včetně diakritiky).

2. **validate_class_name_is_ascii**:
   Eliminuje diakritiku a Unicode symboly. 
   Povoluje: `[a-zA-Z0-9_]`.

3. **validate_class_name_no_underscores**:
   Eliminuje podtržítka. 
   Povoluje: `[a-zA-Z0-9]`.

## Co Python garantuje vždy
I u dynamické tvorby přes `type()` máme garantováno (vyvolá TypeError/ValueError):
- Vstupem je vždy `str`.
- Vstup není nikdy prázdný řetězec `""`.

## Příklady
```python
# OK
validate_class_name_is_identifier("MyClass")      # ✓
validate_class_name_is_identifier("Třída_1")      # ✓ (diakritiku řeší až další krok)

# CHYBA
validate_class_name_is_identifier("123Class")     # ✗ začíná číslem
validate_class_name_is_identifier("My-Class")     # ✗ obsahuje pomlčku
validate_class_name_is_identifier("My Class")     # ✗ obsahuje mezeru
"""