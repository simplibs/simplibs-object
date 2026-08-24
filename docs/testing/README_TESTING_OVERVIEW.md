# 🧪 `testing` — Přehled testovací výbavy

Balíček `simplibs.object.testing` je sada nástrojů pro psaní **vlastních**
testů — ať už testuješ knihovnu samotnou, nebo (mnohem častěji) testuješ
**svoje vlastní** `SimpleConstant`/`SimpleObject` třídy a mixiny ve svém
projektu. Cíl je jednoduchý: napsat jednu čitelnou deklaraci místo desítek
ručně psaných `assert` příkazů, a přitom pokrýt všechny důležité aspekty
chování — dědičnost, tvorbu instance, validaci, reaktivitu, mutabilitu.

---

## 🧭 Obsah

* [Tři vstupní body](#tři-vstupní-body)
* [Společný designový vzor](#společný-designový-vzor)
* [Rychlý start](#rychlý-start)
* [Kde najít co](#kde-najít-co)
* [Doplňkové nástroje mimo `testing`](#doplňkové-nástroje-mimo-testing)

---

## Tři vstupní body

Balíček nabízí tři funkce, každou pro jinou úroveň granularity:

| Funkce | Testuje | Dokument |
|---|---|---|
| **`assert_simple_mixin`** | jeden konkrétní mixin — dědičnost, injekci, sloty/atributy/metody | [README_MIXIN_TESTING.md](README_MIXIN_TESTING.md) |
| **`assert_simple_object`** | jeden blueprint (`SimpleConstant`/`SimpleObject`) — dědičnost, instanciaci, hodnoty, reaktivitu, mutabilitu, lifecycle metody | [README_OBJECT_TESTING.md](README_OBJECT_TESTING.md) |
| **`bulk_test`** | libovolnou dávku obojího najednou, jedním voláním | [README_BULK_TEST.md](README_BULK_TEST.md) |

Typický pracovní postup: začneš s `assert_simple_object`/`assert_simple_mixin`
pro jednotlivé třídy, které zrovna vyvíjíš, a jakmile jich máš víc, přejdeš
na `bulk_test` s dávkou `ObjectCase`/`MixinCase` (nebo i jen holých tuply),
aby celá testovací sada zůstala přehledná v jediném souboru.

[▲ Nahoru](#-obsah)

---

## Společný designový vzor

Všechny tři vstupní body (a jejich vnitřní dílčí asserty) sdílí stejnou
architektonickou filozofii, kterou stojí za to znát předem:

* **Orchestrátor + izolované dílčí asserty.** Každá vysokoúrovňová funkce
  (`assert_simple_mixin`, `assert_simple_object`) je jen sled volání
  malých, jednoúčelových funkcí (`assert_class_inheritance`,
  `assert_value_change`, ...). Dílčí asserty jde použít i samostatně,
  pokud potřebuješ jen jeden konkrétní aspekt otestovat.
* **Fáze: shallow → parameter (opt-in) → deep.** Základní strukturální
  kontroly proběhnou vždy; parametrové testy (reaktivita, mutabilita,
  konkrétní hodnoty) se spustí jen tehdy, pokud jim předáš odpovídající
  argument (sentinel `UNSET` znamená "tohle nechci testovat"); hluboké
  testy (`deep_check=True`, výchozí zapnuté) prověří i vnitřní
  mechanismy jako injekci mixinů nebo `_validate`/`_logic`/`_decompose`.
* **Guard clauses všude, kde by pokračování bylo zavádějící.** Pokud
  vytvoření instance selže, nemá smysl pokračovat na testech, které na
  té instanci staví — každá funkce se po klíčovém kroku ptá "podařilo se
  to?" a pokud ne, ukončí se s jasnou chybou, ne s navazujícím
  `AttributeError`.
* **`maybe_subtest` pro izolované reportování.** Každý logický krok běží
  ve vlastním pytest subtestu (z `simplibs.exception.testing`) — díky
  tomu jedno selhání uprostřed dlouhého testu neschová chyby, které by
  jinak přišly za ním; report ukáže přesně, který konkrétní krok selhal.
* **Sentinel `UNSET` jako "nezajímá mě".** Používá se konzistentně napříč
  celou sadou pro opt-in parametry — stejný sentinel, jaký knihovna
  používá všude jinde (viz
  [`simplibs.sentinels`](../../../simplibs-sentinels/README.md)), ne
  žádná vlastní, jednorázová konvence pro testing.

[▲ Nahoru](#-obsah)

---

## Rychlý start

Otestovat jednu konstantu, včetně mutability a validace:

```python
def test_age(subtests):
    assert_simple_object(
        subtests,
        Age,
        test_value_change=25,
        test_mutability=30,
        test_immutability=40,
    )
```

Otestovat kompozici, včetně obousměrné reaktivity:

```python
def test_full_name(subtests):
    assert_simple_object(
        subtests,
        FullName,
        test_reactivity_up=InnerValue("first_name", "Jana"),
        test_reactivity_down="Petr Novák",
    )
```

Otestovat mixin:

```python
def test_snapshot_mixin(subtests):
    assert_simple_mixin(
        subtests,
        Snapshot,
        test_class=Age,
        method_names=("take_snapshot", "restore_snapshot"),
    )
```

Otestovat celou dávku najednou:

```python
def test_all(subtests):
    bulk_test(subtests, [
        Age,
        (FullName, ()),
        (Snapshot, Age),
        ObjectCase(test_class=Weight, test_mutability=80.5),
    ])
```

[▲ Nahoru](#-obsah)

---

## Kde najít co

```
testing/
├── assert_simple_mixin.py          ──► README_MIXIN_TESTING.md
├── assert_simple_object.py         ──► README_OBJECT_TESTING.md
├── bulk_test.py                    ──► README_BULK_TEST.md
├── asserts/
│   ├── mixins/          (4 funkce)  ──► README_MIXIN_TESTING.md
│   ├── base/             (4 funkce) ──► README_OBJECT_TESTING.md
│   ├── methods/          (3 funkce) ──► README_OBJECT_TESTING.md
│   ├── mutability/       (2 funkce) ──► README_OBJECT_TESTING.md
│   └── reactivity/       (2 funkce) ──► README_OBJECT_TESTING.md
└── containers/
    ├── TestMixin.py                ──► README_BULK_TEST.md
    ├── InnerValue.py               ──► README_BULK_TEST.md
    ├── ObjectCase.py               ──► README_BULK_TEST.md
    └── MixinCase.py                ──► README_BULK_TEST.md
```

[▲ Nahoru](#-obsah)

---

## Doplňkové nástroje mimo `testing`

Dvě sady nástrojů ze složky `tools/` se dobře doplňují s testovací
výbavou, i když formálně nejsou její součástí:

* **[README_AUTOMATE_CREATORS.md](README_AUTOMATE_CREATORS.md)** —
  `create_simple_object`/`create_constant_class`/`create_object_class`
  umožňují vytvořit blueprint **programově**, za běhu. Hodí se to na
  rychlé sestavení testovacích blueprintů přímo uvnitř testu (bez nutnosti
  psát `class` definici v produkčním kódu jen kvůli testu), nebo na
  parametrizované testy generované z dat.
* **[README_RANDOMIZE.md](README_RANDOMIZE.md)** —
  `randomize_value`/`random_data_filler` umí naplnit instanci (nebo celý
  strom kompozice) náhodnými, ale validními hodnotami. To se hodí jako
  doplněk k `assert_simple_object` pro **fuzz testování** — místo ručně
  vybraných testovacích hodnot vyzkoušet chování na mnoha náhodných
  vstupech, včetně stresování reaktivního mechanismu (viz
  [poznámka o reaktivním stress testu](README_RANDOMIZE.md#random_data_filler--celý-strom)).

[▲ Nahoru](#-obsah)
