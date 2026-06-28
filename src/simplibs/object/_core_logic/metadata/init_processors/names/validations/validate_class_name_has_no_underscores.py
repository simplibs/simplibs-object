# Outers
from .....exceptions import SimpleMetadataError


def validate_class_name_has_no_underscores(
    class_name: str
) -> None:
    """
    Validuje, že jméno třídy neobsahuje podtržítko (_).
    
    Doplňková validace po `validate_class_name_is_ascii()`.
    SimpleObject systém nepovoluje podtržítka v názvech tříd.

    ═════════════════════════════════════════════════════════════════
    ⚠️ CLASS NAME CONTAINS UNDERSCORE: Invalid character in name
    ═════════════════════════════════════════════════════════════════
    Expected:  Pouze písmena a číslice (A-Z, a-z, 0-9)
    Got:       {repr(value)} (str)
    Problem:   Název třídy obsahuje podtržítko (_), což není v SimpleObject povoleno.
    Context:   Kontrola metadat potomka SimpleObject třídy.
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Odstraňte podtržítka z názvu třídy.
         • Příklad: Změňte 'My_Class' na 'MyClass' (použijte PascalCase).
         • Podtržítka jsou v systému vyhrazena pro interní účely a odvozená pojmenování.
    ═════════════════════════════════════════════════════════════════
    """

    if "_" in class_name:
        raise SimpleMetadataError(
            error_name="CLASS NAME CONTAINS UNDERSCORE",
            value_label="class_name",
            value=class_name,
            problem="Název třídy obsahuje podtržítko (_), což není v SimpleObject povoleno.",
            expected="Pouze písmena a číslice (A-Z, a-z, 0-9)",
            how_to_fix=(
                "Odstraňte podtržítka z názvu třídy.",
                "Příklad: Změňte 'My_Class' na 'MyClass' (použijte PascalCase).",
                "Podtržítka jsou v systému vyhrazena pro interní účely a odvozená pojmenování."
            ),
            context="Kontrola metadat potomka SimpleObject třídy",
            exception=ValueError
        )


_DESIGN_NOTES = """
# validate_class_name_not_contain_underscore

## Účel
Doplňková validace pro kontrolu přítomnosti podtržítka (_) v názvu SimpleObject třídy.
Určeno pro volání **po** `validate_class_name_is_ascii()`.

SimpleObject systém nepovoluje podtržítka v názvech tříd, protože:
- Podtržítka jsou vyhrazena pro vnitřní účely systému
- Název třídy se používá k automatické derivaci dalších pojmenování
- Podtržítka by mohla kolidovat s odvozovanými atributy a metoda

## Vztah k validate_class_name_is_ascii

Po projití `validate_class_name_is_ascii()` víme, že název obsahuje pouze:

```
[a-zA-Z0-9_]
```

Tato druhá validace **dále omezuje** na:

```
[a-zA-Z0-9]
```

Jednoduše: Pokud `isascii()` projde, zbývá už jen podtržítko z povolených znaků.

## Separace zájmů

Výhodou oddělení do dvou funkcí je:
- **validate_class_name_is_ascii()** — Řeší sémantiku diakritiky (ASCII standard)
- **validate_class_name_not_contain_underscore()** — Řeší projektové pravidlo (SimpleObject convention)

Každá funkce má jasný, jediný zájem — snadno čitelné a testovatelné.

## Příklady

```python
# OK — bez podtržítka
validate_class_name_not_contain_underscore("MyClass")    # ✓
validate_class_name_not_contain_underscore("Class123")   # ✓

# CHYBA — obsahuje podtržítko
validate_class_name_not_contain_underscore("My_Class")   # ✗
validate_class_name_not_contain_underscore("_MyClass")   # ✗
validate_class_name_not_contain_underscore("MyClass_")   # ✗
```

## Poznámky
- Tato funkce se volá **po** `validate_class_name_is_ascii()`.
- V typickém využití se budou obě validace volat za sebou nebo orchestrovat jednou funkcí.
- Po projití obou validací je zaručeno, že název obsahuje **jen** `[a-zA-Z0-9]`.
- Podtržítka se v systému automaticky generují pro odvozená pojmenování,
  proto jejich přítomnost v názvu třídy není povolena.
"""
