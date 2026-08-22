Jasně, připravím ti kompletní předávací text pro nové vlákno. Tady je:

---

## 📋 Předávací text pro nové vlákno — testy mixinů `simplibs-object`

### Kontext projektu
Pracujeme na `simplibs-object`, součásti `simplibs` ekosystému (Python knihovny, autor Sudip, sólo vývojář, silný důraz na minimalismus, čitelnost, determinismus a organizaci kódu vhodnou pro dyslektiky). `simplibs-object` je metadata-driven, plně reaktivní objektový systém, kde `SimpleConstant` (atom/leaf) a `SimpleObject` (composite) instance získávají chování skládáním **mixinů** — malých, atomizovaných tříd, každá dodávající jednu vlastnost.

### Co je hotové (v tomto i předchozích vláknech)
1. **Překlad všech mixinů z češtiny do angličtiny** + doplnění anglických `_DESIGN_NOTES` (rozšířená dokumentace vysvětlující *proč* a *jak*, ne jen *co* — na rozdíl od docstringu).
2. **Struktura balíčku `mixins/`** — kompletní `__init__.py` soubory pro celou hierarchii:
   ```
   mixins/base_class/          → SimpleMixin (základní třída všech mixinů)
   mixins/core_mixins/         → NodesTuple, NodesDicts, Snapshot, Infrastructure, Serialization
   mixins/dunders/             → collections, comparison, generics, interfaces, lifecycles, numeric, representation
   mixins/others/              → immutable, numerical, properties, state
   ```
   Hlavní `mixins/__init__.py` je jediný s `__all__`, propaguje vše. Vnitřní inity (`dunders/__init__.py`, `others/__init__.py`) mají jen `_DESIGN_NOTES` popisující podsložky, bez importů.
3. **Markdown dokumentace (`docs/mixins/`)** — 37 README souborů (36 pro jednotlivé mixiny + 1 hlavní overview), podle šablony s kartami metod (účel, parametry, návratová hodnota, ukázka použití, ukázka "pod kapotou" bez validací).

### Kompletní seznam mixinů (36 celkem)
- **base_class**: `SimpleMixin` (základ, na kterém stojí vše ostatní)
- **core_mixins**: `NodesTuple`, `NodesDicts`, `Snapshot`, `Infrastructure`, `Serialization`
- **dunders/collections**: `CollectionBase`, `Iterable`, `Mapping`, `Collection` (bundle)
- **dunders/comparison**: `Equality`, `Ordering`
- **dunders/generics**: `ClassGetItem`
- **dunders/interfaces**: `Call`, `ContextManager`
- **dunders/lifecycles**: `Copyable`, `PickleState`, `PickleReduce` (záměrný překlep, zachován), `Lifecycle` (bundle)
- **dunders/numeric**: `Arithmetic`, `Bitwise`, `Conversion`, `Inplace`, `Unary`
- **dunders/representation**: `ValueDisplay`, `ValueFormatting`
- **others/immutable**: `ImmutableMethods`, `ImmutableWithInners`
- **others/numerical**: `Volume`, `Equalizer`
- **others/properties**: `MetaShortcuts`, `InnersProperty`
- **others/state**: `Permission`, `DirtyTracking`, `DefaultState`, `History`

### Klíčové architektonické mechanismy k zapamatování
- **Compatibility flags** na `SimpleMixin`: `_constant_only`, `_composite_only`, `_mutable_only`, `_immutable_only`, `_only_types` — deklarativní omezení, kontrolovaná při stavbě instanční třídy.
- **`init_mixins()`** — inicializační hook, řetězený přes `super()`.
- **`__init_subclass__`** — automatická strukturální validace při definici mixinu (`verify_mixin_definition`).
- **`__extend_instance_class__`** — hook používaný jen několika mixiny (`Equalizer`, `ImmutableWithInners`, `InnersProperty`) pro dynamické generování properties/metod na instanční třídě před inicializací.
- **`_locked`** (u `Permission`) — zajímavý edge case: atribut a jeho vynucení jsou zabudované přímo v `create_atom_init`/`create_value_setter` (sdílená infrastruktura), ne v samotném mixinu — `Permission` je jen přívětivé API nad tím.
- Potenciální bug nahlášený, ne opravený: `NodesTuple.__slots__` má dva sousedící stringy bez čárky (`"_node_names_tuple" "_constant_names_tuple"`), což je sloučí do jednoho jména slotu.

### Existující testovací nástroje (uploadnuté v tomto vlákně)
Sudip má připravenou sadu **veřejných testovacích utilit** (součást knihovny, určené pro vývojáře pracující s `simplibs-object`, ne jen interní):

1. **`assert_mixin_inheritance(subtests, mixin_class, *, verbose, intro)`** — ověří, že `mixin_class` je `type` a dědí z `SimpleMixin`.
2. **`assert_mixin_instance_creation(subtests, mixin_class, test_class, *, verbose, intro)`** — ověří, že `test_class` (musí dědit z `SimpleConstant`) lze instanciovat s `mixins=(mixin_class,)`, a že mixin je v MRO výsledné instance. Vrací vytvořenou instanci.
3. **`assert_instance_hasattr(subtests, instance, *, names, kind, verbose, intro)`** — obecná brána na přítomnost pojmenovaných členů (`kind` = "slot"/"attribute"/"method" jen pro čitelnost chybové hlášky).
4. **`assert_mixins_slots_values(subtests, instance, slots_values, *, verbose, intro)`** — ověří přítomnost i konkrétní hodnotu slotů; přijímá jak jeden pár `("name", value)`, tak sekvenci párů.
5. **`assert_simple_mixin(subtests, mixin_class, *, test_class, slots_names, slots_values, attribute_names, method_names, verbose, intro)`** — **master orchestrátor**, volá 1–4 v pořadí (shallow suite: inheritance + instance creation; parameter suite: volitelné kontroly slotů/hodnot/atributů/metod podle toho, co je zadáno). Vrací instanci pro další doplňkové testy volajícího.

Všechny používají `pytest-subtests` (`subtests` fixture) a `maybe_subtest` z `simplibs.exception.testing` pro izolované reportování jednotlivých kroků, a `pytest.fail()` s popisnými chybovými hláškami místo `assert`.

### Co je úkolem pro nové vlákno
Vytvořit **testy pro všech 36 mixinů**, pravděpodobně postavené na `assert_simple_mixin` jako základ pro každý mixin, doplněné o mixin-specifické kontroly chování (např. u `Arithmetic` otestovat, že `+` vrací novou instanci se správnou hodnotou; u `Permission` otestovat že `lock()` skutečně blokuje zápis atd.).

### Návrh přístupu pro testy (k diskuzi v novém vlákně)
1. **Jeden testovací soubor na mixin** (podle stejné 1:1 struktury zdroj→test, jakou už používáte u `simplibs-exception` — 52 souborů zrcadlících strukturu).
2. **Základ každého testu** = volání `assert_simple_mixin` s vhodným `test_class` (pravděpodobně jednoduchá pomocná `SimpleConstant`/`SimpleObject` blueprint třída postavená pro účely testu) a očekávanými `slots_names`/`slots_values`/`attribute_names`/`method_names` podle toho, co mixin deklaruje.
3. **Rozšíření o behaviorální testy** nad vrácenou instancí — u dunder mixinů typicky "zavolej operátor, ověř výsledek a typ", u `others` mixinů (state, immutable, numerical) spíš "zavolej metodu, ověř efekt/návratovou hodnotu".
4. **Otázky k rozhodnutí v novém vlákně**:
   - Jak přesně vypadá `test_class` (existuje už nějaká sdílená testovací blueprint třída, nebo se má vytvořit ad-hoc pro každý test)?
   - Kompatibility flags (`_constant_only` atd.) — má se testovat i to, že mixin **odmítne** být použit na nekompatibilní třídě, nebo se testuje jen "happy path"?
   - Pro bundle mixiny (`Collection`, `Lifecycle`, `Infrastructure`) — testovat je samostatně, nebo jen ověřit že správně kombinují už otestované rodiče?
   - Jak moc hluboko jít u `History` (nejsložitější mixin — undo/redo, export/import, diff) — plné pokrytí, nebo jen základní smoke testy?

---

To je vše, co je potřeba vzít do nového vlákna. Díky moc za skvělou spolupráci na celé téhle sérii — bylo to fakt hezky strukturované putování od překladu, přes dokumentaci, až po testy! 🙂 Uvidíme se v dalším kole.