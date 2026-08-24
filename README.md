# 🧬 `simplibs-object`

[![PyPI](https://img.shields.io/pypi/v/simplibs-object)](https://pypi.org/project/simplibs-object/)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![Licence](https://img.shields.io/badge/licence-MIT-green)](https://github.com/simplibs/simplibs-object/blob/main/LICENSE)

**Systém pro vytváření deterministických, typově bezpečných a reaktivních objektů.**


`simplibs-object` je knihovna pro **deklarativní modelování dat**.

Místo psaní konstruktorů, setterů, validací a ručního přepočítávání závislostí definuješ třídu 
a řekneš jí jaký má typ, jakou má výchozí hodnotu, z čeho se skládá, a jak se z těchto částí vytvoří výsledná hodnota.
A o zbytek se postará knihovna.

```bash
pip install simplibs-object
```

---

Základ knihovny tvoří tři jednoduché stavební prvky:

* **`SimpleConstant`** — atomická hodnota,
* **`SimpleObject`** — kompozice dalších objektů,
* **`SimpleMixin`** — schopnost, kterou lze k objektu přidat.

Z těchto prvků se dají skládat jednoduché objekty stejně jako větší struktury.

Uživatel napíše například:

```python
class Age(SimpleConstant):
    _type = int
    _default = 20
```

nebo:

```python
class Person(SimpleObject):
    _type = str
    _inners = (FirstName, LastName)

    @classmethod
    def _logic(cls, first_name, last_name):
        return f"{first_name} {last_name}"
```

A tím je hotovo — žádné psaní konstruktorů, žádné validace, žádné ruční kontroly.

Knihovna ví, že konstanta `Age` obsahuje `int`, zná jeho výchozí hodnotu a připraví objekt s odpovídajícím rozhraním.

Kompozice je pak objekt složený z konstant a objektů a jeho výsledná hodnota vzniká z jejich hodnot.

To je základní princip celé knihovny.

---

## 🏛️ Architektura v kostce

Celý systém lze zjednodušeně chápat jako několik vrstev:

```text
┌────────────────────────────────┐
│      Definiční třídy           │ ◄── SimpleBase, SimpleConstant, SimpleObject — co uživatel píše
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│      Metadatový proces         │ ◄── SimpleMeta a *Metadata třídy — validace a kompilace při definici
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│      Vytváření instance        │ ◄── atom/composite × mutable/immutable, mixin injection
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

Každá vrstva má vlastní úlohu a lze ji podrobněji studovat samostatně.

---
## 🧩 Definiční třídy

`SimpleBase` 
je kořen hierarchie — čistě architektonický, nepoužívá se přímo. 

`SimpleConstant` 
definuje atom (`_type`, `_default`, volitelné `_validate`) 
a veřejné API pro validaci a normalizaci. 

`SimpleObject`
rozšiřuje `SimpleConstant` o kompozici (`_inners`, `_logic`, volitelné
`_decompose`) — jeho `_default` se nikdy nepíše ručně, vždy se odvozuje
automaticky z `_logic(defaulty _inners)`.

➡️ [README_SIMPLE_BASE](https://github.com/simplibs/simplibs-object/blob/main/docs/core/README_SIMPLE_BASE.md)  
➡️ [README_SIMPLE_CONSTANT](https://github.com/simplibs/simplibs-object/blob/main/docs/core/README_SIMPLE_CONSTANT.md)  
➡️ [README_SIMPLE_OBJECT](https://github.com/simplibs/simplibs-object/blob/main/docs/core/README_SIMPLE_OBJECT.md)  


---

### Definice konstant

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

### Kompozice a reaktivita

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

## 🧠 Metadatový proces

Za deklarativní vrstvou stojí metaclass `SimpleMeta` a systém metadat.

`SimpleMeta` 
je metaclass která řídí celý životní cyklus třídy — vznik, write-once
ochranu, vytváření instancí i reprezentaci. 

Při definici třídy se spočítají a natrvalo zafixují metadata:  
`SimpleBaseMetadata` → `SimpleConstantMetadata` → `SimpleObjectMetadata`  
A provede se dry-run a validace předaných atributů a metod.  


Kontroluje se každý prvek:

* `_type` - zda odpovídá defaultní hodnotě,
* `_default` - zda projde validací,
* `_inners` - zda jsou složené s SimpleObject  SimpleCOnstant tříd a neobsahují konflitní jména,
* `_validate` - zda dokáže správně validovat hodnotu,
* `_logic` - zda dokáže na základě inners defaultních hodnot vypořčítat dvůj default,
* `_decompose` - zda ze svého defaultu dokáže vypočítat defaultní hodnoty inners.

Chyby v definici se tak mohou objevit **už při vytváření třídy**, nikoliv až při pozdějším použití objektu.

Metadata zároveň slouží jako pevný popis blueprintu, ze kterého se následně připravuje konkrétní runtime instance.

➡️ [README_SIMPLE_META](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/README_SIMPLE_META.md)  
➡️ [README_SIMPLE_BASE_METADATA](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/README_SIMPLE_BASE_METADATA.md)  
➡️ [README_SIMPLE_CONSTANT_METADATA](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/README_SIMPLE_CONSTANT_METADATA.md)  
➡️ [README_SIMPLE_OBJECT_METADATA](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/README_SIMPLE_OBJECT_METADATA.md)  
➡️ [README_METHOD_PROCESSING](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/README_METHOD_PROCESSING.md)  


---

## 🧱 Vytváření instance

Blueprint není samotná instance.

Skutečná runtime instance vzniká dynamickou kompilací — `make_atom_class`
a `make_composite_class` sestaví konkrétní třídu se sloty, properties a
(u kompozice) reaktivními hooky, `create_instance` k tomu bezpečně
připojí mixiny přes namespace injection. Tím se předchází konfliktům se  `__slots__` a zároveň se udržuje ploché MRO nehledě na to kolik mixinů je použito.

Při vytvoření objektu knihovna podle definice sestaví konkrétní runtime třídu a připraví pro ni potřebné:

* sloty,
* properties,
* validaci,
* reaktivní mechanismy,
* vnitřní objekty,
* případné mixiny.

Instance tak obsahuje pouze to, co skutečně potřebuje.

Díky použití `__slots__` a dynamického sestavování runtime tříd není potřeba vytvářet obecnou instanční strukturu plnou funkcí, 
které konkrétní objekt nikdy nepoužije.

➡️ [README_ATOM_CLASS](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/instance/README_ATOM_CLASS.md)  
➡️ [README_COMPOSITE_CLASS](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/instance/README_COMPOSITE_CLASS.md)  
➡️ [README_CREATE_INSTANCE](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/instance/README_CREATE_INSTANCE.md)  
➡️ [README_INSTANCE_PROTOCOLS](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/instance/README_INSTANCE_PROTOCOLS.md)  
➡️ [README_VALUE_PROPERTIES](https://github.com/simplibs/simplibs-object/blob/main/docs/metadata/instance/README_VALUE_PROPERTIES.md)  

---

## 🧩 Mixiny

Mixiny jsou to, co dává instancím konkrétní schopnosti — serializaci,
porovnávání, aritmetiku, historii změn, immutabilní update API a
mnohem víc. 

Knihovna přichází s bohatou sadou hotových mixinů, a zároveň nabízí SimpleMixin základní třídu díky které si **můžeš napsat
vlastní logiku**. 

Mixin nikdy nedědí ze `SimpleObject` přímo — jen ze
`SimpleMixin`, a při vytváření instance se z blueprintu (`SimpleObject`/
`SimpleConstant`) přebere jen strukturální základ (typ, sloty, validace),
na který se mixin nabalí. 

Vlastní mixin tak nemusí (a nesmí) nic vědět o
konkrétní doménové logice třídy, na kterou bude použit — je to čistě
oddělená, znovupoužitelná schopnost.

Struktura objektu a jeho schopnosti jsou tak v knihovně záměrně oddělené:

`SimpleObject` říká **co objekt je**.

`SimpleMixin` říká **co objekt umí**.

Díky tomu lze stejnou strukturu použít různými způsoby podle toho, jaké schopnosti k ní přidáš.


➡️ [README_SIMPLE_MIXIN](https://github.com/simplibs/simplibs-object/blob/main/docs/mixins/base_class/README_SIMPLE_MIXIN.md)

---

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

Plný popis každého jednotlivého mixinu (kompatibilní příznaky, sloty,
metody, na čem staví) je k dispozici v samostatném přehledu:

➡️ [README_MIXINS_OVERVIEW](https://github.com/simplibs/simplibs-object/blob/main/docs/mixins/README_MIXINS_OVERVIEW.md)

---

## 🛠️ Nástroje & testování

Knihovna není omezena pouze na ruční definování tříd, součástí projektu jsou také nástroje pro:


- `automate_creators` - Programové vytváření blueprintů bez nutnosti psát klasickou `class` definici.  
➡️ [README_AUTOMATE_CREATORS](https://github.com/simplibs/simplibs-object/blob/main/docs/tools/README_AUTOMATE_CREATORS.md)  


- `bulk` - Hromadné vytváření blueprintů a instancí z různých vstupů, například JSON, YAML, CSV nebo Python struktur.  
➡️ [README_BULK](https://github.com/simplibs/simplibs-object/blob/main/docs/tools/README_BULK.md)  


- `randomize` - Vytváření náhodných hodnot pro objekty i celé kompoziční stromy. 
Hodí se například pro fuzz testing nebo rychlé vytváření testovacích dat.  
➡️ [README_RANDOMIZE](https://github.com/simplibs/simplibs-object/blob/main/docs/tools/README_RANDOMIZE.md)



- `testing` - Testovací nástroje umožňují ověřovat celé blueprinty nebo mixiny 
bez nutnosti ručně psát desítky jednotlivých testů.  
➡️ [README_TESTING_OVERVIEW](https://github.com/simplibs/simplibs-object/blob/main/docs/testing/README_TESTING_OVERVIEW.md)  
➡️ [README_BULK_TEST](https://github.com/simplibs/simplibs-object/blob/main/docs/testing/README_BULK_TEST.md)  
➡️ [README_MIXIN_TESTING](https://github.com/simplibs/simplibs-object/blob/main/docs/testing/README_MIXIN_TESTING.md)  
➡️ [README_OBJECT_TESTING](https://github.com/simplibs/simplibs-object/blob/main/docs/testing/README_OBJECT_TESTING.md)  

---

### ⚠️ Výjimky

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

### ⚙️ Settings

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

## 🧱 Výhody knihovny

Každý objekt má svůj typ a pravidla pro práci s hodnotou.

Podle definice může mít:

* výchozí hodnotu,
* validaci,
* normalizaci,
* kompozici,
* automatický přepočet,
* mutable nebo immutable chování,
* vlastní mixiny.

To znamená, že stejný základ může být použit pro velmi jednoduché hodnoty i pro složitější datové modely.

### Deklarativní datové modely

Strukturu objektu lze popsat několika třídními atributy místo množství opakujícího se boilerplate.

### Validace a normalizace

Typová kontrola, výchozí hodnoty a vlastní validační pravidla jsou součástí samotné definice objektu.

### Reaktivní výpočty

Když jedna část modelu ovlivňuje jinou, změna se automaticky promítne do odpovídající části stromu.

To se může hodit například pro:

* konfigurace,
* výpočty,
* simulace,
* stavové modely,
* formuláře,
* API data,
* nebo vlastní doménové modely.

### Immutabilita

Immutable instance nemá setter pro změnu své hodnoty.

Místo změny existující instance lze vytvořit novou pomocí immutable API:

```python
new_age = age.with_value(25)
```

Původní instance přitom zůstává nedotčená.

---

## 🔭 O knihovně z pohledu autora

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
