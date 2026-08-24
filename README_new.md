# 🧬 `simplibs-object`

[![PyPI](https://img.shields.io/pypi/v/simplibs-object)](https://pypi.org/project/simplibs-object/)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![Licence](https://img.shields.io/badge/licence-MIT-green)](https://github.com/simplibs/simplibs-object/blob/main/LICENSE)

**Systém pro vytváření deterministických, typově bezpečných, reaktivních objektů.**

Místo psaní konstruktorů, validací a ručních kontrol napíšeš jen deklaraci —
`_type`, `_default`, `_inners`, `_logic` — a zbytek (validace, defaulty,
obousměrná reaktivita, immutabilita, rozšiřitelnost přes mixiny) se
postará samo.

```python
from simplibs.object import SimpleConstant, SimpleObject

class FirstName(SimpleConstant):
    _type = str
    _default = "Jan"

class LastName(SimpleConstant):
    _type = str
    _default = "Novák"

class FullName(SimpleObject):
    _type = str
    _inners = (FirstName, LastName)

    @classmethod
    def _logic(cls, first_name, last_name):
        return f"{first_name} {last_name}"

person = FullName()
person.first_name = "Petr"   # → person.value se automaticky přepočítá
```

---

## 🧭 Co tahle knihovna vlastně je

Je to **mini-framework pro deklarativní modelování dat**, postavený na
třech pojmech: **atomických konstantách** (`SimpleConstant`), **kompozicích**
(`SimpleObject`) a **mixinech** (`SimpleMixin`), které se skládají jako lego
kostky.

Napíšeš třídu s pár deklarativními atributy, a metaclass (`SimpleMeta`) za
tebe:

* zvaliduje typy, defaulty, `_inners` i vlastní logiku už při definici
  třídy — chyba v tvém kódu se odhalí hned při importu, ne až za běhu,
* vytvoří kompletní, izolovanou instanci s vlastními sloty, vlastnostmi a
  metodami — dynamicky, ale bezpečně (přes `type(...)`, nikdy přes `exec`),
* zapojí **obousměrnou reaktivitu**: změna v jednom vnitřním prvku se
  probublá až ke kořeni kompozice; změna kořene se rozloží zpátky do
  jednotlivých prvků,
* umožní ti přidat **mutabilitu nebo immutabilitu**, a libovolnou
  kombinaci mixinů, které vdechnou instanci konkrétní schopnosti.

Instance přitom není odtržená od svého blueprintu — nese si v sobě
odkaz na třídu, ze které vznikla, i na data, se kterými byla vytvořená.
Trochu to připomíná **miniaturní formu digitálního života** — objekt
schopný reprodukce (`with_*` funkce v immutabilním pipeline, `Copyable`
mixin) i vývoje (`History`, `DirtyTracking`, mixiny nad `Stepper`) —
sebereplikovatelný prvek se schopností dalšího vývoje. Je to jen drobná
poznámka pod čarou k hlavnímu účelu knihovny, ale je to přesně ten detail,
který mě na celém návrhu bavil nejvíc. 🙂

### Proč by tě to mělo zajímat

* **Validace a normalizace zadarmo.** Každá konstanta má typ, default,
  validaci a normalizaci, aniž bys cokoliv z toho psal ručně.
* **Reaktivní výpočty.** Změna v jedné části modelu se automaticky
  propaguje celým stromem — ideální pro konfigurace, finanční modely,
  simulace, stavové stroje.
* **Immutabilita bez bolesti.** Immutable instance nemá setter vůbec —
  je to garance na úrovni Pythonu, ne jen konvence. Změny se dělají přes
  `with_*` funkce, které vrací novou, konzistentní instanci.
* **Rozšiřitelnost přes mixiny**, bez zásahu do jádra — a bez limitů
  klasické vícenásobné dědičnosti (žádné konflikty `__slots__`, žádné
  MRO peklo).
* **Extrémně lehké instance** — `__slots__` všude, žádný zbytečný
  `__dict__`, dynamicky kompilované třídy vznikají líně a jen jednou za
  danou kombinaci parametrů.

---

## 🚀 Rychlý start

```bash
pip install simplibs-object
```

```python
from simplibs.object import SimpleConstant

class Age(SimpleConstant):
    _type = int
    _default = 18

    @classmethod
    def _validate(cls, value, *, return_bool=False):
        if value < 0:
            return cls.bool_or_raise_validate_error(
                value, "Věk nemůže být záporný.", return_bool=return_bool
            )
        return True

age = Age()               # mutable instance, hodnota = 18
age.value = 25             # OK
age.value = -1              # SimpleRuntimeError

frozen_age = Age(mutable=False)
frozen_age.value = 30       # AttributeError — immutable nemá setter
```

Kompletní příklad s kompozicí a mixiny najdeš v [Rychlém startu testovací
sady](docs/testing/README_TESTING_OVERVIEW.md#rychlý-start) — nejrychlejší
cesta, jak vidět knihovnu v akci na reálném kódu.

---

## 🏛️ Architektura: 5 pilířů

```
┌────────────────────────────────┐
│      Definiční třídy           │ ◄── SimpleConstant, SimpleObject — co uživatel píše
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│      Metadatový proces         │ ◄── SimpleBase, SimpleMeta a *Metadata třídy — validace a kompilace při definici
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│      Runtime instance          │ ◄── atom/composite × mutable/immutable, mixin injection
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│            Mixiny              │ ◄── volitelné schopnosti - rozšiřitelnost bez zásahu do jádra
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│     Nástroje & testování       │ ◄── automate_creators, randomize, a nástoje pro testování
└────────────────────────────────┘
```

### 1. Definiční třídy

`SimpleBase` je kořen hierarchie — čistě architektonický, nepoužívá se
přímo. `SimpleConstant` definuje atom (`_type`, `_default`, volitelné
`_validate`) a veřejné API pro validaci a normalizaci. `SimpleObject`
rozšiřuje `SimpleConstant` o kompozici (`_inners`, `_logic`, volitelné
`_decompose`) — jeho `_default` se nikdy nepíše ručně, vždy se odvozuje
automaticky z `_logic(defaulty _inners)`.

➡️ [docs/core/README_SIMPLE_BASE.md](docs/core/README_SIMPLE_BASE.md)
➡️ [docs/core/README_SIMPLE_CONSTANT.md](docs/core/README_SIMPLE_CONSTANT.md)
➡️ [docs/core/README_SIMPLE_OBJECT.md](docs/core/README_SIMPLE_OBJECT.md)

### 2. Metadatový proces

Metaclass `SimpleMeta` řídí celý životní cyklus třídy — vznik, write-once
ochranu, vytváření instancí i reprezentaci. Při definici třídy se spočítají
a natrvalo zafixují metadata (`SimpleBaseMetadata` → `SimpleConstantMetadata`
→ `SimpleObjectMetadata`), včetně dry-run validace `_validate`/`_logic`/
`_decompose` — jakákoliv chyba v uživatelské logice se odhalí hned při
importu.

➡️ [docs/metadata/README_SIMPLE_META.md](docs/metadata/README_SIMPLE_META.md)
➡️ [docs/metadata/README_SIMPLE_BASE_METADATA.md](docs/metadata/README_SIMPLE_BASE_METADATA.md)
➡️ [docs/metadata/README_SIMPLE_CONSTANT_METADATA.md](docs/metadata/README_SIMPLE_CONSTANT_METADATA.md)
➡️ [docs/metadata/README_SIMPLE_OBJECT_METADATA.md](docs/metadata/README_SIMPLE_OBJECT_METADATA.md)
➡️ [docs/metadata/README_METHOD_PROCESSING.md](docs/metadata/README_METHOD_PROCESSING.md)

### 3. Vytváření instance

Skutečná runtime instance vzniká dynamickou kompilací — `make_atom_class`
a `make_composite_class` sestaví konkrétní třídu se sloty, properties a
(u kompozice) reaktivními hooky, `create_instance` k tomu bezpečně
připojí mixiny přes namespace injection (ne přes klasickou vícenásobnou
dědičnost — to by narazilo na konflikty `__slots__`).

➡️ [docs/metadata/instance/README_ATOM_CLASS.md](docs/metadata/instance/README_ATOM_CLASS.md)
➡️ [docs/metadata/instance/README_COMPOSITE_CLASS.md](docs/metadata/instance/README_COMPOSITE_CLASS.md)
➡️ [docs/metadata/instance/README_CREATE_INSTANCE.md](docs/metadata/instance/README_CREATE_INSTANCE.md)
➡️ [docs/metadata/instance/README_INSTANCE_PROTOCOLS.md](docs/metadata/instance/README_INSTANCE_PROTOCOLS.md)
➡️ [docs/metadata/instance/README_VALUE_PROPERTIES.md](docs/metadata/instance/README_VALUE_PROPERTIES.md)

### 4. Mixiny

Mixiny jsou to, co dává instancím konkrétní schopnosti — serializaci,
porovnávání, aritmetiku, historii změn, immutabilní update API a
mnohem víc. Knihovna přichází s bohatou sadou hotových mixinů (viz
[přehled níže](#-mixiny)), ale hlavní síla je v tom, že si **můžeš napsat
vlastní**. Mixin nikdy nedědí ze `SimpleObject` přímo — jen ze
`SimpleMixin`, a při vytváření instance se z blueprintu (`SimpleObject`/
`SimpleConstant`) přebere jen strukturální základ (typ, sloty, validace),
na který se mixin nabalí. Vlastní mixin tak nemusí (a nesmí) nic vědět o
konkrétní doménové logice třídy, na kterou bude použit — je to čistě
oddělená, znovupoužitelná schopnost.

➡️ [docs/mixins/base_class/README_SIMPLE_MIXIN.md](docs/mixins/base_class/README_SIMPLE_MIXIN.md) — kontrakt pro psaní vlastních mixinů

#### Přehled dostupných mixinů

| Kategorie | Co poskytují |
|---|---|
| **Core mixiny** | `NodesTuple`, `NodesDicts`, `Snapshot`, `Infrastructure`, `Serialization` — sdílená infrastruktura, na které staví skoro vše ostatní. |
| **Dunders — Collections** | `CollectionBase`, `Iterable`, `Mapping`, `Collection` — dict-like/iterovatelné chování nad `_inners`. |
| **Dunders — Comparison** | `Equality`, `Ordering` — `__eq__`/`__hash__`/`__lt__`/... podle hodnoty. |
| **Dunders — Generics** | `ClassGetItem` — `MyClass[int]` syntaxe pro typing/IDE. |
| **Dunders — Interfaces** | `Call`, `ContextManager` — `__call__`, `__enter__`/`__exit__`. |
| **Dunders — Lifecycles** | `Copyable`, `PickleState`, `PicleReduce`, `Lifecycle` — kopírování a pickling přes snapshot. |
| **Dunders — Numeric** | `Arithmetic`, `Unary`, `Bitwise`, `Inplace`, `Conversion` — celá paleta číselných operátorů. |
| **Dunders — Representation** | `ValueDisplay`, `ValueFormatting` — `__repr__`/`__str__`/`format()`/`__bool__`. |
| **Others — Immutable** | `ImmutableMethods`, `ImmutableWithInners` — `with_constant`/`with_composite`/`with_changes` API a per-inner zkratky. |
| **Others — Numerical** | `Volume`, `Equalizer` — bezpečné, ohraničené číselné "stepování". |
| **Others — Properties** | `InnersProperty`, `MetaShortcuts` — ergonomický přístup k `_inners` a metadatům. |
| **Others — State** | `DefaultState`, `DirtyTracking`, `History`, `Permission` — správa stavu mutable instancí, včetně plného undo/redo. |

Plný popis každého jednotlivého mixinu (kompatibilní příznaky, sloty,
metody, na čem staví) je v samostatném přehledu:

➡️ [docs/mixins/README_MIXINS_OVERVIEW.md](docs/mixins/README_MIXINS_OVERVIEW.md)

### 5. Nástroje a testování

* **`automate_creators`** — vytvoření blueprintu programově, za běhu,
  bez psaní `class` definice (`create_simple_object`, `create_constant_class`,
  `create_object_class`).
* **`bulk`** — hromadné vytváření blueprintů/instancí z JSON, YAML, CSV,
  tabulky, nebo přímo z Pythonu (`BulkCase`).
* **`randomize`** — propojení s [`simplibs-randomize`](https://github.com/simplibs/simplibs-randomize)
  pro naplnění instance (i celého stromu kompozice) validními náhodnými
  hodnotami — užitečné pro fuzz testování.
* **`testing`** — kompletní testovací sada (`assert_simple_object`,
  `assert_simple_mixin`, `bulk_test`) pro ověřování tvých vlastních
  blueprintů i mixinů jedním voláním místo desítek ručních assertů.

➡️ [docs/tools/README_AUTOMATE_CREATORS.md](docs/tools/README_AUTOMATE_CREATORS.md)
➡️ [docs/tools/README_BULK.md](docs/tools/README_BULK.md)
➡️ [docs/tools/README_RANDOMIZE.md](docs/tools/README_RANDOMIZE.md)
➡️ [docs/testing/README_TESTING_OVERVIEW.md](docs/testing/README_TESTING_OVERVIEW.md)
➡️ [docs/testing/README_BULK_TEST.md](docs/testing/README_BULK_TEST.md)
➡️ [docs/testing/README_MIXIN_TESTING.md](docs/testing/README_MIXIN_TESTING.md)
➡️ [docs/testing/README_OBJECT_TESTING.md](docs/testing/README_OBJECT_TESTING.md)

---

## ⚠️ Výjimky

Všechny chyby, které knihovna vyhazuje, dědí ze společného kořene
`SimpleObjectError` (postaveného na [`simplibs-exception`](https://github.com/simplibs/simplibs-exception) —
strukturované, čitelné diagnostické karty místo holého tracebacku).
Díky tomu jde zachytit **jakoukoliv** chybu z knihovny jedním
`except SimpleObjectError`, nebo cíleně jen jednu konkrétní kategorii:

| Výjimka | Kdy nastane |
|---|---|
| `SimpleDefinitionError` | Chyba v **definici třídy** — špatně napsaný `_inners`, zakázaný `_default` na kompozici, neplatná signatura `_logic`. Nastává při importu/definici třídy. |
| `SimpleInitializationError` | Chyba při **vytváření instance** — neplatné parametry `mixins`/`mutable`, nekompatibilní mixin, selhání sestavení vnitřních prvků. |
| `SimpleRuntimeError` | Chyba v **datech nebo za běhu** — neplatná hodnota při zápisu, selhání `_validate`, pokus o zápis do immutable instance. Tohle je výjimka, na kterou nejčastěji narazíš při běžném používání. |

```python
from simplibs.object.exceptions import SimpleObjectError

try:
    age.value = -5
except SimpleObjectError as e:
    print(e)  # strukturovaná diagnostická karta: co, proč, jak opravit
```

`SimpleObjectError` navíc filtruje interní snímky knihovny ze stopy
chyby (`_skip_locations`) — chybová hláška ukazuje na **tvůj** kód, ne
na vnitřní implementaci knihovny.

---

## ⚙️ Settings

Knihovna má jedno konfigurovatelné místo — logování. Žádné automatické
nastavování handlerů, žádný zásah do root loggeru; vše je opt-in a plně
pod tvojí kontrolou.

```python
import logging
logging.getLogger("simple").setLevel(logging.DEBUG)
```

Navíc lze zaregistrovat vlastní callback, který se spustí při každé
změně hodnoty (`value = ...` na kořenové úrovni):

```python
import simplibs.object.settings.logging as simple_logging

def my_callback(cls, value, event):
    print(f"{cls.__name__}: {event} -> {value}")

simple_logging.on_value_change = my_callback
```

---

## 🔭 Kam s tím dál

Knihovna vznikla z jednoduchého pozorování — opakujícího se vzorce
"typ + default + validace + logika" — a z touhy dát mu jednou provždy
deterministický, znovupoužitelný základ. Je to trochu jako vlastní malý
jazyk pro domluvu s Pythonem: minimum logiky, maximum využitelnosti.
Každý parametr funkce se stává vlastním objektem, a dohromady tvoří
reaktivní systém.

Sám ji plánuju použít jako základ pro připravovanou `simplibs-validate`
— validační logika, kde je `SimpleConstant` s vlastní `_validate` přesně
ten správný stavební kámen. Ale potenciál vidím širší: protože libovolnou
konstantu lze přidáním `_inners` proměnit v kompozici a libovolnou
kompozici naopak zjednodušit na konstantu (odebráním `_inners`, nebo
vytvořením instance s `as_atom=True`), dá se knihovna použít i jako
obecný **deklarativní stavební systém** — od nejmenších jednotek nahoru,
oběma směry rozšiřitelný a specifikovatelný. Jedna z myšlenek, kterou
bych rád časem vyzkoušel: použít konstanty jako elementární stavební
prvky a přes kompozice z nich sestavovat popisy atomů a molekul —
doslova, ne v přeneseném programátorském smyslu.

Tohle je **první verze** — výsledek všech původních myšlenek, ale
rozhodně ne uzavřené dílo. Je to spíš pevný základ a struktura, na které
je radost dál stavět, než hotový produkt. Skutečné použití časem ukáže,
co ještě potřebuje doladit, rozšířit, nebo úplně předělat.

---

## ☯️ O simplibs

Všechny knihovny v ekosystému **simplibs** (Simple Libraries) sdílí
společnou inženýrskou filozofii:

* **Přívětivé k dyslektikům:** Aktivně minimalizujeme kognitivní zátěž.
  Kód je atomizovaný do malých, samostatných jednotek, soubory jsou
  pojmenované přímo podle úlohy, kterou plní, a vysvětlení popisují spíš
  *proč* je něco navržené tak, jak je, ne jen *co* to dělá.
* **Programátorský klid:** Nic by nemělo chybět a nic by nemělo přebývat.
  Ceníme si čistých cest provedení a srozumitelné architektury před
  uspěchanou, neuspořádanou sadou funkcí.
* **Defenzivní styl:** Aktivně předjímáme okrajové případy a chybové
  stavy, aby zůstaly jen bezpečné cesty provedení. Kód je stavěný na to,
  aby elegantně degradoval, ne aby nečekaně spadl.
* **Minimalismus:** Najít nejpřímější cestu k cíli v co nejméně krocích,
  bez ústupků na bezpečnosti, čitelnosti nebo úplnosti.
* **Kód jako řemeslo:** Kód by měl být příjemný na pohled, čitelný na
  první pohled a vyvolávat strukturální harmonii. Bereme softwarové
  inženýrství jako přesné řemeslo.

---

### 🤝 Přispívání a komunita

Tohle je **open-source projekt**, dělaný s láskou a péčí. Velmi si
vážíme spolupráce s komunitou a uvítáme jakoukoliv zpětnou vazbu, hlášení
chyb, nebo nápady na nové funkce!

* **Chceš přispět?** Klidně otevři Issue nebo pošli Pull Request.
* **Chceš se ozvat?** Pokud chceš projekt dál probrat, spolupracovat,
  nebo se jen pozdravit, otevři GitHub Issue nebo založ Discussion.

---

### 📝 Licence

Tahle knihovna je vydaná pod licencí **MIT**. Stavěj skvělé věci!

---

[▲ Zpět nahoru](#-simplibs-object)
