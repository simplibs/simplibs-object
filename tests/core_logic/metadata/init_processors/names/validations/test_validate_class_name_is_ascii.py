# Outers
from .....exceptions import SimpleMetadataError


def validate_class_name_is_ascii(
    class_name: str
) -> None:
    """
    Validuje, že jméno třídy obsahuje pouze ASCII znaky (bez diakritiky).
    
    Určeno pro validaci názvů tříd získaných z již vytvořeného objektu (ClassName.__name__).
    Pracuje s předpokladem, že třída již prošla Python definicí a základními kontrolami.

    ═════════════════════════════════════════════════════════════════
    ⚠️ CLASS NAME NOT ASCII: Non-standard characters detected
    ═════════════════════════════════════════════════════════════════
    Expected:  Pouze základní ASCII znaky (A-Z, a-z, 0-9, _)
    Got:       {repr(value)} (str)
    Problem:   Název třídy obsahuje nepovolené znaky (diakritiku nebo symboly).
    Context:   Kontrola metadat potomka SimpleObject třídy.
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Třída má neplatný název — nejspíše byla vytvořena dynamicky se špatným vstupem.
         • Odstraňte z názvu háčky a čárky (např. 'Měna' -> 'Mena').
         • Kontaktujte správce systému.
    ═════════════════════════════════════════════════════════════════
    """

    if not class_name.isascii():
        raise SimpleMetadataError(
            error_name="CLASS NAME NOT ASCII",
            label="class_name",
            value=class_name,
            problem="Název třídy obsahuje nepovolené znaky (diakritiku nebo symboly).",
            expected="Pouze základní ASCII znaky (A-Z, a-z, 0-9, _)",
            how_to_fix=(
                "Třída má neplatný název — nejspíše byla vytvořena dynamicky se špatným vstupem.",
                "Odstraňte z názvu háčky a čárky (např. 'Měna' -> 'Mena').",
                "Kontaktujte správce systému."
            ),
            context="Kontrola metadat potomka SimpleObject třídy",
            exception=ValueError
        )


_DESIGN_NOTES = """
# validate_class_name_is_ascii

## Účel
Validuje, že jméno třídy SimpleObject obsahuje pouze ASCII znaky bez diakritiky.
Určeno pro kontrolu názvů tříd získaných z již vytvořeného objektu (`ClassName.__name__`).

Tato validace pracuje s vědomím, že třída již prošla Python definicí,
a tudíž máme zaručeny určité základní vlastnosti.

## Co Python již garantuje (při normální definici třídy)

Když napíšeš `class ClassName:` a Python jí dovolí vytvořit, pak máš zaručeno:

1. **Typ je str** — `ClassName.__name__` vždy vrátí řetězec
2. **Není prázdné** — Python nikdy nedovolí `class :`
3. **Je to validní identifikátor** — Projde `isidentifier()` s jistotou
   - Obsahuje jen: písmena, číslice, podtržítko
   - Nespojuje se s číslem (`class 2MyClass:` = ERROR)
   - Bez mezer, pomlček, teček (`class My-Class:` = ERROR)
4. **Není klíčové slovo** — Python to při definici neopeř (`class class:` = ERROR)

Všechny tyto kontroly **nemusíme dělat znovu** — Python je již prověřil!

## Co zbývá po vynechání těchto kontrol?

Po tom, co Python garantuje `isidentifier()`, obsahuje název:

```
Jen: [a-zA-Z0-9_]
```

Nic více. Žádné jiné znaky nejsou v Python identifikátoru možné.

## Co kontrolujeme my — ASCII znaky

Kontrolujeme `isascii()` — Je-li true, garantujeme:
- ✓ Pouze znaky ASCII tabulky (0-127)
- ✓ Žádná diakritika (háčky, čárky)
- ✓ Žádné Unicode symboly

**Prakticky to znamená:** Pokud projde `isascii()`, obsah je stále jen:

```
[a-zA-Z0-9_]
```

Protože jiné znaky by `isidentifier()` neprošly (Python to už dělal).

## Příklady

```python
# OK — ASCII, bez diakritiky
validate_class_name_is_ascii("MyClass")      # ✓
validate_class_name_is_ascii("Class123")     # ✓
validate_class_name_is_ascii("My_Class")     # ✓

# CHYBA — není ASCII (diakritika)
validate_class_name_is_ascii("Třída")        # ✗ háček
validate_class_name_is_ascii("Mesíc")        # ✗ čárka
validate_class_name_is_ascii("Ελληνικά")     # ✗ řečtina
```

## Poznámky
- Tato kontrola je **první ze dvou doplňkových validací** pro SimpleObject.
- Po projití `isascii()` obsahuje název pouze znaky `[a-zA-Z0-9_]`.
- Druhá doplňková kontrola `validate_class_name_not_contain_underscore()`
  dále zakazuje podtržítko, čímž zbyde pouze `[a-zA-Z0-9]`.
- Separace na dvě funkce umožňuje jasnou separaci zájmů
  a snadnější čitelnost kódu.
"""
