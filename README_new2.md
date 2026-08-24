# 🧬 `simplibs-object`

[![PyPI](https://img.shields.io/pypi/v/simplibs-object)](https://pypi.org/project/simplibs-object/)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![Licence](https://img.shields.io/badge/licence-MIT-green)](https://github.com/simplibs/simplibs-object/blob/main/LICENSE)

**Systém pro vytváření deterministických, typově bezpečných a reaktivních objektů.**

`SimpleObject` umožňuje popsat datový objekt několika málo deklaracemi a zbytek nechat na knihovně.

Místo opakovaného psaní konstruktorů, validací, normalizace, setterů a přepočítávání závislostí stačí definovat, **co objekt je a z čeho se skládá**. Knihovna z této definice vytvoří konzistentní objekt s připraveným rozhraním, validací a reaktivním chováním.

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

person.first_name = "Petr"

assert person.value == "Petr Novák"
```

V tomto příkladu jsou `FirstName` a `LastName` jednoduché atomické prvky. `FullName` je kompozice, která z nich vytváří výslednou hodnotu.

A právě v tom spočívá základní myšlenka knihovny:

> **Definuj strukturu a pravidla. Knihovna se postará o zbytek.**

---

## 🧭 Co je `simplibs-object`

`Simplibs-object` je **deklarativní systém pro modelování datových objektů**.

Je postavený na několika jednoduchých stavebních prvcích:

* **`SimpleConstant`** — atomický objekt s typem, výchozí hodnotou a případnou validací,
* **`SimpleObject`** — objekt, který svou hodnotu vytváří z dalších objektů,
* **`SimpleMixin`** — samostatné schopnosti, které lze k objektu přidávat podle potřeby.

Z těchto několika prvků lze sestavit jednoduché atomy stejně jako rozsáhlé stromové kompozice.

Každá definice přitom funguje jako **blueprint**. Určuje strukturu a pravidla objektu, zatímco skutečné runtime instance jsou vytvářeny až podle konkrétní konfigurace.

---

## 🧩 Od deklarace k objektu

Když vytvoříš například:

```python
class Age(SimpleConstant):
    _type = int
    _default = 18
```

nemusíš už ručně vytvářet konstruktor, ukládat hodnotu, kontrolovat její typ ani psát setter.

Knihovna z definice odvodí potřebné chování.

```python
age = Age()

age.value = 25
```

Pokud je potřeba přidat vlastní pravidlo, lze ho jednoduše doplnit:

```python
class Age(SimpleConstant):
    _type = int
    _default = 18

    @classmethod
    def _validate(cls, value, *, return_bool=False):
        if value < 0:
            return cls.bool_or_raise_validate_error(
                value,
                "Věk nemůže být záporný.",
                return_bool=return_bool,
            )
        return True
```

Tím vzniká objekt, který zná svůj typ, výchozí hodnotu i pravidla pro platné hodnoty.

---

## 🔄 Kompozice a reaktivita

Síla knihovny se začne výrazněji projevovat ve chvíli, kdy objekty začnou být složené z dalších objektů.

`SimpleObject` definuje:

* `_inners` — z jakých objektů se skládá,
* `_logic` — jak z nich vzniká výsledná hodnota,
* `_decompose` — jak lze výslednou hodnotu případně rozložit zpět.

Například:

```python
class FullName(SimpleObject):
    _type = str
    _inners = (FirstName, LastName)

    @classmethod
    def _logic(cls, first_name, last_name):
        return f"{first_name} {last_name}"
```

Změna vnitřní hodnoty se automaticky promítne do kompozice:

```python
person.first_name = "Petr"

# person.value == "Petr Novák"
```

A pokud kompozice podporuje `_decompose`, může fungovat i opačný směr:

```text
          ┌───────────────┐
          │   FullName    │
          │ "Petr Novák"  │
          └───────┬───────┘
                  │
             _decompose
              ↙       ↘
       ┌──────────┐ ┌─────────┐
       │ FirstName│ │LastName │
       │  "Petr"  │ │ "Novák" │
       └──────────┘ └─────────┘
```

Knihovna tak vytváří **obousměrně reaktivní strom hodnot**:

* změna uvnitř se propaguje směrem ke kořeni,
* změna kompozice se může rozložit směrem k jejím částem.

Důležitou vlastností je přitom determinismus — přepočet není založený na skrytém systému událostí nebo magických závislostech. Vztahy mezi částmi jsou určeny samotnou definicí objektu.

---

## 🧠 Metadata a kontrola definice

Za deklarativní vrstvou stojí metaclass `SimpleMeta` a systém metadat.

Při definici třídy se kontrolují například:

* typy,
* výchozí hodnoty,
* `_inners`,
* signatury metod,
* `_validate`,
* `_logic`,
* `_decompose`.

Chyby v definici se tak mohou objevit **už při vytváření třídy**, nikoliv až při pozdějším použití objektu.

Metadata zároveň slouží jako pevný popis blueprintu, ze kterého se následně připravuje konkrétní runtime instance.

➡️ [SimpleMeta](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/README_SIMPLE_META.md)
➡️ [SimpleBaseMetadata](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/README_SIMPLE_BASE_METADATA.md)
➡️ [SimpleConstantMetadata](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/README_SIMPLE_CONSTANT_METADATA.md)
➡️ [SimpleObjectMetadata](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/README_SIMPLE_OBJECT_METADATA.md)
➡️ [Zpracování metod](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/README_METHOD_PROCESSING.md)

Podrobnější popis samotných definičních tříd:

➡️ [SimpleBase](https://github.com/simplibs/simplibs-object/blob/main/docs/core/README_SIMPLE_BASE.md)
➡️ [SimpleConstant](https://github.com/simplibs/simplibs-object/blob/main/docs/core/README_SIMPLE_CONSTANT.md)
➡️ [SimpleObject](https://github.com/simplibs/simplibs-object/blob/main/docs/core/README_SIMPLE_OBJECT.md)

---

## 🧱 Runtime instance

Blueprint není samotná instance.

Při vytvoření objektu knihovna podle definice sestaví konkrétní runtime třídu a připraví pro ni potřebné:

* sloty,
* properties,
* validaci,
* reaktivní mechanismy,
* vnitřní objekty,
* případné mixiny.

Instance tak obsahuje pouze to, co skutečně potřebuje.

Díky použití `__slots__` a dynamického sestavování runtime tříd není potřeba vytvářet obecnou instanční strukturu plnou funkcí, které konkrétní objekt nikdy nepoužije.

➡️ [Atomické runtime třídy](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/instance/README_ATOM_CLASS.md)
➡️ [Kompozitní runtime třídy](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/instance/README_COMPOSITE_CLASS.md)
➡️ [Vytváření instancí](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/instance/README_CREATE_INSTANCE.md)
➡️ [Instance protokoly](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/instance/README_INSTANCE_PROTOCOLS.md)
➡️ [Value properties](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/instance/README_VALUE_PROPERTIES.md)

---

## 🧩 Mixiny: schopnosti oddělené od struktury

Struktura objektu a jeho schopnosti jsou v knihovně záměrně oddělené.

`SimpleObject` říká **co objekt je**.

`SimpleMixin` říká **co objekt umí**.

Díky tomu lze stejnou strukturu použít různými způsoby podle toho, jaké schopnosti k ní přidáš.

Knihovna například nabízí mixiny pro:

* kolekce,
* porovnávání,
* číselné operace,
* reprezentaci,
* kopírování,
* serializaci,
* historii změn,
* immutable update,
* práci se stavem,
* a další chování.

A stejně důležité je, že **vlastní mixiny lze jednoduše vytvářet**.

Mixin nemusí znát konkrétní doménovou logiku objektu. Přidává pouze vlastní, izolovanou schopnost.

➡️ [SimpleMixin — kontrakt pro vlastní mixiny](https://github.com/simplibs/simplibs-object/blob/main/docs/mixins/base_class/README_SIMPLE_MIXIN.md)

### Přehled dostupných mixinů

| Kategorie          | Co poskytují                                                              |
| ------------------ | ------------------------------------------------------------------------- |
| **Core**           | `NodesTuple`, `NodesDicts`, `Snapshot`, `Infrastructure`, `Serialization` |
| **Collections**    | `CollectionBase`, `Iterable`, `Mapping`, `Collection`                     |
| **Comparison**     | `Equality`, `Ordering`                                                    |
| **Generics**       | `ClassGetItem`                                                            |
| **Interfaces**     | `Call`, `ContextManager`                                                  |
| **Lifecycles**     | `Copyable`, `PickleState`, `PicleReduce`, `Lifecycle`                     |
| **Numeric**        | `Arithmetic`, `Unary`, `Bitwise`, `Inplace`, `Conversion`                 |
| **Representation** | `ValueDisplay`, `ValueFormatting`                                         |
| **Immutable**      | `ImmutableMethods`, `ImmutableWithInners`                                 |
| **Numerical**      | `Volume`, `Equalizer`                                                     |
| **Properties**     | `InnersProperty`, `MetaShortcuts`                                         |
| **State**          | `DefaultState`, `DirtyTracking`, `History`, `Permission`                  |

➡️ [Kompletní přehled mixinů](https://github.com/simplibs/simplibs-object/blob/main/docs/mixins/README_MIXINS_OVERVIEW.md)

---

## 🛠️ Další stavební nástroje

Knihovna není omezena pouze na ruční definování tříd.

Součástí projektu jsou také nástroje pro:

### `automate_creators`

Programové vytváření blueprintů bez nutnosti psát klasickou `class` definici.

➡️ [Automate creators](https://github.com/simplibs/simplibs-object/blob/main/docs/tools/README_AUTOMATE_CREATORS.md)

### `bulk`

Hromadné vytváření blueprintů a instancí z různých vstupů, například JSON, YAML, CSV nebo Python struktur.

➡️ [Bulk](https://github.com/simplibs/simplibs-object/blob/main/docs/tools/README_BULK.md)

### `randomize`

Propojení se [`simplibs-randomize`](https://github.com/simplibs/simplibs-randomize), které umožňuje vytvářet validní náhodné hodnoty pro objekty i celé kompoziční stromy.

Hodí se například pro fuzz testing nebo rychlé vytváření testovacích dat.

➡️ [Randomize](https://github.com/simplibs/simplibs-object/blob/main/docs/tools/README_RANDOMIZE.md)

### `testing`

Testovací nástroje umožňují ověřovat celé blueprinty nebo mixiny bez nutnosti ručně psát desítky jednotlivých testů.

➡️ [Testing overview](https://github.com/simplibs/simplibs-object/blob/main/docs/testing/README_TESTING_OVERVIEW.md)
➡️ [Bulk testing](https://github.com/simplibs/simplibs-object/blob/main/docs/testing/README_BULK_TEST.md)
➡️ [Mixin testing](https://github.com/simplibs/simplibs-object/blob/main/docs/testing/README_MIXIN_TESTING.md)
➡️ [Object testing](https://github.com/simplibs/simplibs-object/blob/main/docs/testing/README_OBJECT_TESTING.md)

---

## 🚀 Rychlý start

Instalace:

```bash
pip install simplibs-object
```

Jednoduchý atom:

```python
from simplibs.object import SimpleConstant


class Age(SimpleConstant):
    _type = int
    _default = 18

    @classmethod
    def _validate(cls, value, *, return_bool=False):
        if value < 0:
            return cls.bool_or_raise_validate_error(
                value,
                "Věk nemůže být záporný.",
                return_bool=return_bool,
            )
        return True


age = Age()

age.value = 25
```

Instance mohou být mutable nebo immutable:

```python
age = Age()
age.value = 25

frozen_age = Age(mutable=False)
```

Immutable instance nemá setter pro změnu hodnoty. Změny se místo toho provádějí pomocí immutable API, které vytváří novou konzistentní instanci.

Kompletní příklad kompozice a mixinů najdeš v:

➡️ [Rychlý start testovací sady](https://github.com/simplibs/simplibs-object/blob/main/docs/testing/README_TESTING_OVERVIEW.md#rychlý-start)

---

## 🏛️ Architektura v kostce

Celý systém lze zjednodušeně chápat jako několik vrstev:

```text
┌───────────────────────────────┐
│       Definiční třídy          │
│ SimpleBase / Constant / Object │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│        Metadata & Meta         │
│   validace + zpracování        │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│       Runtime instance         │
│ atom / composite / mutability  │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│            Mixiny              │
│      volitelné schopnosti      │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│       Nástroje & testing       │
└───────────────────────────────┘
```

Každá vrstva má vlastní úlohu a lze ji podrobněji studovat samostatně.

---

## ⚠️ Výjimky

Všechny chyby knihovny vycházejí ze společného kořene `SimpleObjectError`, který je postavený na [`simplibs-exception`](https://github.com/simplibs/simplibs-exception).

To umožňuje zachytit všechny chyby knihovny společně:

```python
from simplibs.object.exceptions import SimpleObjectError

try:
    age.value = -5
except SimpleObjectError as error:
    print(error)
```

Základní kategorie jsou:

| Výjimka                     | Kdy nastane                                          |
| --------------------------- | ---------------------------------------------------- |
| `SimpleDefinitionError`     | Chyba v definici třídy.                              |
| `SimpleInitializationError` | Chyba při vytváření instance.                        |
| `SimpleRuntimeError`        | Chyba při práci s hodnotou nebo během běhu instance. |

Výjimky zároveň filtrují interní části knihovny ze stopy chyby, takže diagnostika směřuje především k místu, kde problém skutečně vznikl v uživatelském kódu.

---

## ⚙️ Settings

Knihovna má jedno hlavní konfigurovatelné místo — logování.

Nenastavuje automaticky handlery ani nezasahuje do root loggeru. Logování je opt-in a zůstává plně pod kontrolou aplikace.

```python
import logging

logging.getLogger("simple").setLevel(logging.DEBUG)
```

Lze také zaregistrovat vlastní callback reagující na změnu hodnoty:

```python
import simplibs.object.settings.logging as simple_logging


def my_callback(cls, value, event):
    print(f"{cls.__name__}: {event} -> {value}")


simple_logging.on_value_change = my_callback
```

---

## 🔭 Kam knihovna směřuje

`Simplibs-object` vznikl kolem jednoduchého opakujícího se vzorce:

```text
typ
 +
default
 +
validace
 +
logika
```

Z tohoto malého základu lze postupně vytvářet větší struktury.

Atom může být samostatným objektem. Několik atomů může vytvořit kompozici. Kompozice může být součástí další kompozice. A jednotlivým objektům lze podle potřeby přidávat schopnosti prostřednictvím mixinů.

Výsledkem je systém, který lze používat od velmi malých stavebních prvků až po komplexní reaktivní datové struktury.

Knihovna je stále otevřeným projektem a její další směr bude do značné míry určovat skutečné používání. Některé části jsou už pevně ustálené, jiné se budou přirozeně dál vyvíjet společně s tím, jak se bude ukazovat, kde je tento přístup skutečně užitečný.

---

## ☯️ O simplibs

Všechny knihovny v ekosystému **simplibs** (Simple Libraries) sdílí společnou inženýrskou filozofii:

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

Tohle je **open-source projekt** a zpětná vazba, hlášení chyb i nové nápady jsou vítané.

* **Chceš přispět?** Otevři Issue nebo pošli Pull Request.
* **Chceš se ozvat?** Pro diskuzi, spolupráci nebo jen pozdrav můžeš využít GitHub Issue nebo Discussion.

### 📝 Licence

Tahle knihovna je vydaná pod licencí **MIT**.

---

[▲ Zpět nahoru](#-simplibs-object)
