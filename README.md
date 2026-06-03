# simplibs-object

# Dokumentace projektu: SimpleObject

`SimpleObject` je univerzální knihovna pro tvorbu striktně definovaných parametrických tříd. Původně vznikla pro potřeby konfigurace logování, ale vyvinula se v robustní systém („švýcarský nůž“) pro metaprogramování a dynamickou tvorbu objektů, které jsou deterministicky dopočítávány z minimální deklarace.

## 1. Základní filozofie
* **Minimalismus:** Stačí definovat typ, výchozí hodnotu a případně vnitřní strukturu (`inners`).
* **Determinismus:** Všechny ostatní metody a vlastnosti jsou z těchto dat pevně dopočítány.
* **Defenzivní programování:** Systém obsahuje silné validace (v rámci `Metadata`), které odhalí chyby v definici třídy ještě před jejím spuštěním.
* **Kompozice nad dědičností:** Objekty se skládají z „Atomů“ (základní hodnoty) a „Kompozic“ (vnořené `SimpleObject` třídy).

## 2. Rozhraní pro definici (Uživatel)
Uživatel definuje svou třídu děděním od `SimpleObject` a specifikací následujících atributů a metod:

### Atributy třídy
* `_type`: (Povinný) Určuje datový typ hodnoty.
* `_DEFAULT`: (Povinný pro atomy) Výchozí hodnota. Nesmí být `None`.
* `_inners`: (Volitelný) Tuple dalších tříd typu `SimpleObject`, které tvoří strukturu kompozice.
* `__metadata__`: Obsahuje instanci `SimpleObjectMetadata` pro interní validaci.

### Logické metody
* `_logic()`: Definuje, jak se z `inners` vypočítá výsledná hodnota (u atomů vrací `_DEFAULT`).
* `_decompose(value)`: (Volitelná) Rozloží komplexní hodnotu zpět na parametry pro `inners`.
* `_validate(value)`: (Volitelná) Doplňková validace nad rámec typové kontroly.

## 3. Automaticky generované rozhraní
Knihovna na základě definice poskytuje tyto standardizované metody:

* `is_valid(value)` / `validate(value)`: Kontrola validity a typu.
* `normalize(value)`: Převede vstup na validní formát.
* `create_value(**kwargs)`: Vytvoří hodnotu pomocí `_logic`.
* `decompose_value(value)`: Rozloží hodnotu pomocí `_decompose`.
* `update_value(value, **kwargs)`: Aktualizuje existující hodnotu.

## 4. Architektura generování tříd (Pipeline)
`SimpleObject` využívá vrstvenou strukturu pro dynamickou tvorbu instančních tříd:

### A. SimpleCore (`CORE()`)
Vytváří nízkoúrovňové „hodnotové jádro“.
* Zapouzdřuje surovou hodnotu do vlastnosti `value`.
* Zajišťuje normalizaci při zápisu.
* Využívá `__slots__` pro efektivitu.

### B. SimpleInstance (`INSTANCE()`)
Vytváří atomickou instanci se specifickým pojmenováním.
* Mapuje hodnotu na unikátní jméno (např. podle `snake_case` názvu třídy).
* Zajišťuje, aby nedocházelo ke kolizím jmen v rámci kompozic.
* Implementuje `__init__` se správnou signaturou (díky `simple-signature`).

### C. SimpleMixin (`MIXIN()`)
Řeší rekurzivní skládání u kompozitních tříd.
* Pokud má třída `inners`, `MIXIN()` posbírá jejich instanční třídy a spojí je do jednoho celku.
* Výsledkem je třída, která má v `__init__` parametry pro všechny vnořené objekty.

### D. SimpleObject (`OBJECT()`)
Koncová továrna na objekty.
* Umožňuje uživateli vybrat si sadu funkčních Mixinů (např. pro serializaci, porovnávání, matematické operace).
* Dynamicky skládá finální třídu z: `InstanceBase` + `Funkční Mixiny` + `Základní hodnota/Mixin`.

## 5. Ukázka struktury Mixinů
Knihovna disponuje bohatou sadou připravených modulů, které lze k objektu připojit:
* **Dunders:** `Equality`, `Comparable`, `Hashable`, `Iterable`, `Arithmetic`.
* **Logic:** `Serialization` (JSON, Dict), `Mutation`, `History`, `State`.
* **Protocols:** `ContextManager`, `Callable`.

---

---

## About the simplibs ecosystem

**Dyslexia-friendly** — minimise mental load. Atomise code into self-contained
units, name files after the logic they contain, write explanations that describe
*why* — not just *what*.

**Programmer's zen** — nothing should be missing and nothing should be
superfluous. The journey is the destination: code should be fully understood;
better to go slowly and correctly than quickly and with mistakes. The
crystallisation approach — not perfection on the first try, but gradual
refinement towards it.

**Defensive style** — anticipate all possible failure modes so that only safe
paths remain. Never raise unexpected errors; degrade gracefully.

**Minimalism** — find the path to the goal in as few steps as possible, but
leave nothing out. Each file has one responsibility.

**Code as craft** — code should be pleasant to look at and evoke a sense of
harmony. Treat code as a small work of art — like a carpenter carving a
sculpture. Optimise for the user: everything should make sense without having
to study the documentation at length.

These are aspirations — a sense of direction. And that is exactly what the
note about the journey becoming the destination is all about. 🙂

---

*The library is covered by tests across all modules. Tests are part of the
repository and serve as living documentation of the expected behaviour.*