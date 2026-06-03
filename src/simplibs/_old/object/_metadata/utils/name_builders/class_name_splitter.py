# Outers
from .validations import (
    validate_class_name_is_identifier,
    validate_class_name_is_ascii,
    validate_class_name_has_no_underscores
)



def class_name_splitter(class_name: str) -> tuple[str, ...]:
    """
    Rozdělí název třídy SimpleObject na sémantické jednotky (slova).

    Tato utilita je šitá na míru ekosystému SimpleObject a předpokládá, že název
    byl získán přímo z atributu třídy `__name__`. Provádí specifické validace,
    které doplňují garantované vlastnosti Pythonu.
    """

    # 1. Validace jména třídy
    # Provádíme pouze nezbytné kontroly, které Python parser u __name__ negarantuje.
    if not class_name.isidentifier() or not class_name.isascii() or "_" in class_name:
        validate_class_name_is_identifier(class_name)
        validate_class_name_is_ascii(class_name)
        validate_class_name_has_no_underscores(class_name)

    # 2. Inicializace úložiště pro slova a akumulátoru znaků
    words = []
    char_stack = []

    # 3. Pomocná funkce pro vyprázdnění zásobníku a uložení slova
    def flush_stack() -> None:
        """
        Vytáhne aktuální slovo z char_stack, normalizuje ho a přidá do seznamu.
        Zásobník následně vyčistí.
        """
        if char_stack:
            word = "".join(char_stack)
            # Akronymy (všechna velká) zůstávají, ostatní se převedou na malá.
            normalized_word = word if word.isupper() else word.lower()
            words.append(normalized_word)
            char_stack.clear()

    # 4. Iterace přes jednotlivé znaky názvu třídy
    for char in class_name:

        # 4.1 Číslice: Začínají vždy nové slovo (User123 -> user, 123)
        if char.isdigit():

            # 4.1.1 Přechod z písmene na číslici → ukončit aktuální slovo
            if char_stack and not char_stack[-1].isdigit():
                flush_stack()

            # 4.1.2 Přidání číslice do zásobníku
            char_stack.append(char)

        # 4.2 Velká písmena: Potenciální start slova nebo akronymu (PascalCase)
        elif char.isupper():

            # 4.2.1 Přechod z malého písmena nebo číslice na velké → ukončit slovo
            if char_stack and (char_stack[-1].islower() or char_stack[-1].isdigit()):
                flush_stack()

            # 4.2.2 Přidání velkého písmene do zásobníku
            char_stack.append(char)

        # 4.3 Malá písmena: Pokračování slova nebo detekce konce akronymu
        else:
            # 4.3.1 Detekce akronymu: Pokud je v zásobníku více znaků a poslední je velký,
            # pak toto velké písmeno patří k novému slovu (např. 'HTTPServer' -> 'HTTP', 'Server')
            if len(char_stack) > 1 and char_stack[-1].isupper():
                last_uppercase = char_stack.pop()   # Vyjmout start nové slova
                flush_stack()                       # Uzavřít akronym
                char_stack.append(last_uppercase)   # Začít nové slovo

            # 4.3.2 Přidání malého písmene do zásobníku
            char_stack.append(char)

    # 5. Zpracování posledního slova zbývajícího v akumulátoru
    flush_stack()

    # 6. Vrácení n-tice sémantických slov
    return tuple(words)


_DESIGN_NOTES = """
# class_name_splitter

## Účel
Specializovaná utilita pro dekompozici názvů tříd na sémantické jednotky (slova). 
V rámci ekosystému SimpleObject slouží jako základní stavební kámen pro generování 
čitelných názvů, atributů a parametrů.

## Logika a tok zpracování
Funkce používá přístup **stavového zásobníku** (`char_stack`) a zpracovává vstupní 
řetězec znak po znaku. Je optimalizována pro PascalCase bez podtržítek.

### Manipulace se znaky
1. **Číslice**: Fungují jako body přechodu. Pokud následují po písmenech, začínají 
   vždy nový blok (např. `User123` -> `user`, `123`).
2. **Velká písmena**: Označují začátek nového slova v PascalCase nebo součást akronymu.
3. **Malá písmena**: Pokračování běžného slova nebo indikátor konce akronymu.

### Detekce akronymů (4.3.1)
Když přijde malé písmeno a v zásobníku jsou velká písmena (více než jedno):
- Poslední velké písmeno v zásobníku patří k začínajícímu slovu.
- Předchozí velká písmena tvoří akronym, který se uzavře.
- Příklad: `HTTPServer` -> Zásobník akumuluje `['H','T','T','P']` -> přijde 's' 
  -> vyjme 'P', uzavře 'HTTP', začne nové slovo s `['P','s']`.

Díky tomu získáváme čisté výsledky:
- `JSONParser` -> `('json', 'parser')`
- `MyHTTPClient` -> `('my', 'http', 'client')`

## Normalizace výstupu
Pomocná funkce `flush_stack()` aplikuje pravidlo zachování významu:
- Sekvence složené pouze z velkých písmen (akronymy) zůstávají velká.
- Ostatní slova (PascalCase) jsou převedena na malá písmena.
- To umožňuje snadnou následnou transformaci (např. na snake_case).

## Proč je flush_stack() vnořená
- **Sdílený stav**: Má přímý přístup k `char_stack` a `words` bez režie parametrů.
- **Lokalita**: Je to implementační detail, který patří výhradně do této logiky.

## Validace a integrita
Funkce se spoléhá na to, že vstup pochází z `ClassName.__name__`. Přesto provádí 
tři doplňkové validace pro případ dynamicky tvořených tříd přes `type()`:
1. **is_identifier**: Chytne nelegální znaky jako mezery nebo pomlčky.
2. **is_ascii**: Vyloučí diakritiku (háčky, čárky), která by zničila logiku rozdělování.
3. **no_underscores**: Vynutí čistý PascalCase, což zjednodušuje algoritmus (nemusíme řešit `_`).

## Rozhodnutí u okrajových případů
| Případ | Chování | Odůvodnění |
|---|---|---|
| Prázdné jméno | Vyvolá ValueError (přes type()) | Python nedovolí existenci třídy bez názvu. |
| Čísla uprostřed | `('http2', 'server')` | Čísla tvoří bloky; přechod zpět na písmeno vyvolá flush. |
| Jedno písmeno | `('a',)` | Minimální platný případ funguje správně. |
| Dynamický šum | Zachycen validací | Ochrana před `type("Moje Trida", ...)` |

## Výkonové poznámky
- **Časová složitost**: O(n), kde n je délka názvu třídy.
- **Prostorová složitost**: O(w), kde w je počet slov ve výsledku.
- Algoritmus je lineární a provede pouze jeden průchod řetězcem.
"""