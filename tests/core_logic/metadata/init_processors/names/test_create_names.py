from typing import TYPE_CHECKING
# Inners
from .class_name_splitter import class_name_splitter
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def create_names(
    owner_class: "SimpleClassLike"
) -> tuple[tuple[str, ...], str, str]:
    """
    Procesní pipeline pro generování deterministických názvů třídy.

    Tato funkce transformuje název třídy do různých textových podob používaných
    napříč systémem (od uživatelských popisů až po privátní atributy).
    Validaci názvu třídy deleguje na `class_name_splitter`.
    """
    class_name = owner_class.__name__

    # 1. Dekompozice názvu na jednotlivá slova (provádí i validaci názvu třídy)
    # Pipeline začíná rozkladem na sémantické jednotky (tuple slov).
    name_tuple = class_name_splitter(class_name)

    # 2. Vytvoření snake_case verze pro parametry (např. v __init__)
    # Standardní Python konvence pro proměnné a argumenty.
    name_snake = "_".join(name_tuple).lower()

    # 3. Vytvoření privátní verze pro vnitřní sloty a atributy
    # Technické jméno pro vnitřní integritu objektu.
    name_private = "_" + name_snake

    # 4. Navrácení tuple s vytvořenými názvy
    return (
        name_tuple,
        name_snake,
        name_private
    )


_DESIGN_NOTES = """
# create_names

## Účel
Tato funkce funguje jako **procesní pipeline**, která definuje identitu `SimpleObject` 
v různých kontextech. Jejím cílem je zajistit absolutní determinismus — každý název 
v systému (od parametru v konstruktoru až po zprávu ve výjimce) je přímo a 
předvídatelně odvozen od názvu třídy.

## Architektonický koncept (Pipeline)
Funkce je záměrně navržena jako lineární tok transformací. 
- **Delegace validace**: Pipeline neřeší, zda je jméno třídy správné. Tuto odpovědnost 
  přenáší na `class_name_splitter`. Pokud splitter vrátí tuple slov, pipeline má 
  zaručeno, že pracuje s čistými daty.
- **Separace zájmů**: `create_names` se soustředí výhradně na formátování a sémantický 
  význam jednotlivých podob jmen.

## Význam generovaných jmen

| Název | Formát | Hlavní využití |
|-------|--------|----------------|
| `name_readable` | `moje slova` | Textové popisy, lidsky čitelný výstup ve výjimkách. |
| `name_title` | `Moje slova` | Začátky vět v hlášeních, titulky v UI nebo dokumentaci. |
| `name_snake` | `moje_slova` | Názvy parametrů v `__init__`, lokální proměnné, klíče v JSON. |
| `name_private` | `_moje_slova` | Názvy vnitřních slotů a privátních atributů třídy. |

## Síla SimpleObject determinismu
Hlavní předností tohoto přístupu je, že vývojář nemusí ručně definovat názvy 
atributů nebo popisků. Tím, že systém vynutí správný název třídy (přes validace 
v dekompozici), automaticky garantuje:
1. **Konzistenci**: Parametr v API se bude vždy jmenovat stejně jako proměnná v kódu.
2. **Bezchybnost**: Odpadají překlepy při ručním přepisování jmen.
3. **Předvídatelnost**: Pohledem na název třídy lze okamžitě určit, jak vypadá 
   její privátní úložiště nebo jak se bude tvářit navenek.

## Technické detaily
- **Zachování zkratek**: Při tvorbě `name_title` nepoužíváme standardní `capitalize()`, 
  protože ta by převedla vše kromě prvního písmene na malá (HTTP -> Http). Naše 
  implementace `name_readable[0].upper() + name_readable[1:]` respektuje akronymy 
  vytvořené splitterem.
- **Bezpečné spojování**: Pipeline počítá s tím, že splitter již odstranil 
  veškerý syntaktický šum (podtržítka, diakritiku), takže operace jako `join` 
  jsou bezpečné a předvídatelné.
"""