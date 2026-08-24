# 📋 Instanční protokoly — Co instance umí v základu

Tenhle dokument je referenční přehled toho, co má **čerstvě vytvořená
instance k dispozici, ještě než se k ní připojí jediný mixin**. Je to
"prázdný stůl" — základní rozhraní, na které mixiny teprve nabalují další
schopnosti (viz sekce Mixiny).

Existují čtyři varianty, podle dvou nezávislých os popsaných v
[README_CREATE_INSTANCE.md](README_CREATE_INSTANCE.md#get_base_class--výběr-strukturálního-základu):

|  | **Mutable** | **Immutable** |
|---|---|---|
| **Atomická** (`SimpleConstant`) | [Atomická mutable](#1-atomická-mutable-instance) | [Atomická immutable](#2-atomická-immutable-instance) |
| **Kompozitní** (`SimpleObject`) | [Kompozitní mutable](#3-kompozitní-mutable-instance) | [Kompozitní immutable](#4-kompozitní-immutable-instance) |

Kompozitní varianty **dědí vše** z odpovídající atomické varianty (mutable
z mutable, immutable z immutable) — viz
[README_COMPOSITE_CLASS.md](README_COMPOSITE_CLASS.md) — takže se to
v tabulkách níže neopakuje, jen odkazuje.

---

## 🧭 Obsah

* [1. Atomická mutable instance](#1-atomická-mutable-instance)
* [2. Atomická immutable instance](#2-atomická-immutable-instance)
* [3. Kompozitní mutable instance](#3-kompozitní-mutable-instance)
* [4. Kompozitní immutable instance](#4-kompozitní-immutable-instance)

---

## 1. Atomická mutable instance

Vytvoří se voláním `MyConstant()` (výchozí — `mutable=True`).

### Sloty (interní stav)

| Slot | Popis |
|---|---|
| `_value` | Aktuální normalizovaná hodnota. |
| `_owner` | Odkaz na rodičovskou kompozici, pokud je tenhle atom jejím vnitřním prvkem. Jinak `UNSET`. |
| `_locked` | Příznak zámku (`False` u čerstvé instance). |
| `__weakref__` | Podpora slabých referencí (z `InstanceBase`). |

### Veřejné rozhraní

| Člen | Typ | Popis |
|---|---|---|
| `value` | property (čtení/zápis) | Hlavní přístup k hodnotě. Zápis normalizuje, uloží a spustí bublání nahoru, pokud má instance vlastníka. |
| `owner` | property (jen čtení) | Vrací `_owner`. |
| `meta` | property (jen čtení) | Metadata blueprintu, ze kterého instance vznikla (`SimpleConstantMetadata`). |
| `init_mixins()` | metoda | Prázdný hook (bez mixinů nic nedělá). |
| `validate_type(value, ...)` | classmethod\* | Zděděno z blueprintu — deterministická typová validace. |
| `validate(value, ...)` | classmethod\* | Zděděno z blueprintu — plná validace (typ + `_validate`). |
| `is_valid(value)` | classmethod\* | Zděděno z blueprintu — boolean varianta `validate`. |
| `normalize(value, ...)` | classmethod\* | Zděděno z blueprintu — normalizace vstupu. |
| `__repr__()` | metoda | Diagnostický výpis: jméno třídy, blueprint path, aktuální hodnota, adresa v paměti. |
| `__str__()` | metoda | Jméno třídy. |

\* Tyto metody instance **dědí přímo z uživatelské blueprint třídy**
(`meta.owner_class`), protože `make_atom_class` staví instanci na dvojí
dědičnosti `(InstanceBase, meta.owner_class)` — viz
[README_ATOM_CLASS.md](README_ATOM_CLASS.md#make_atom_class--kompilace-atomické-třídy).
Fungují stejně, jako když se volají přímo na blueprintu, jen teď je volá
konkrétní instance.

### Co na instanci **není** (odstraněno při kompilaci)

`_type`, `_default`, `_validate` (jako přepisatelný hook — validace samotná
zůstává dostupná přes `validate`/`is_valid`), `bool_or_raise_validate_error`
— tohle jsou deklarativní artefakty blueprintu, které instance po
kompilaci nemá (viz
[README_ATOM_CLASS.md](README_ATOM_CLASS.md#make_atom_class--kompilace-atomické-třídy)).

[▲ Nahoru](#-obsah)

---

## 2. Atomická immutable instance

Vytvoří se voláním `MyConstant(mutable=False)`. Vyžaduje, aby hodnota typu
`_type` byla hashovatelná (kontrolováno v `create_instance`).

### Rozdíly oproti mutable variantě

| Člen | Rozdíl |
|---|---|
| `value` | Property má **jen getter**. Pokus o zápis (`instance.value = ...`) skončí `AttributeError` už na úrovni Pythonu — setter se pro immutable variantu vůbec nevytváří. |
| `_root_value_setter` | **Neexistuje.** Tahle metoda se přidává do `class_dict` jen podmíněně, `if mutable` (viz [README_ATOM_CLASS.md](README_ATOM_CLASS.md#create_root_value_setter--reaktivní-zápis-hodnoty)). |

Vše ostatní (sloty, `owner`, `meta`, validační metody, `__repr__`/`__str__`)
je stejné jako u mutable varianty.

[▲ Nahoru](#-obsah)

---

## 3. Kompozitní mutable instance

Vytvoří se voláním `MyObject()`. Dědí **vše** z
[atomické mutable instance](#1-atomická-mutable-instance) — sloty
`_value`/`_owner`/`_locked`, `owner`, `meta`, validační metody,
`__repr__`/`__str__`. Tabulka níže ukazuje jen to, co přidává navíc.

### Sloty navíc

Jeden privátní slot pro **každý přímý vnitřní prvek** deklarovaný
v `_inners` — např. pro `_inners = (Engine, Wheels)` vzniknou sloty
`_engine`, `_wheels`, každý obsahující instanci daného vnitřního prvku.

### Veřejné rozhraní navíc

| Člen | Typ | Popis |
|---|---|---|
| `value` | property (čtení/zápis, **přepsáno**) | Getter stejný princip jako u atomu. Setter navíc vyžaduje `meta.is_decomposeable`, po zápisu automaticky rozešle novou hodnotu do vnitřních prvků (`_recalculate_inners`). |
| `<jméno_inner>` | property (čtení/zápis*) | Pro každý přímý vnitřní prvek — přímý přístup k jeho hodnotě, např. `instance.engine`. Zápis podléhá stejným pravidlům jako `value` toho konkrétního prvku (atomický/kompozitní podle jeho vlastní povahy). |
| `<jméno_inner>_instance` | property (jen čtení) | Přístup k samotné instanci vnitřního prvku, ne k jeho hodnotě, např. `instance.engine_instance`. |
| `calculate_value(*args, **kwargs)` | classmethod\* | Zděděno z blueprintu — spočítá hodnotu z parametrů odpovídajících `_inners`. |
| `decompose_value(value)` | classmethod\* | Zděděno z blueprintu — rozloží hodnotu zpět na díly pro `_inners` (jen pokud `is_decomposeable`). |
| `_recalculate_self()` | metoda (interní) | Přepočítá vlastní hodnotu z aktuálních hodnot dětí a bublá nahoru. |
| `_recalculate_inners()` | metoda (interní) | Rozloží vlastní hodnotu a rozešle díly dětem. |

\* Stejně jako u atomu — zděděno z uživatelské blueprint třídy.

> **Poznámka k `<jméno_inner>` properties:** přesný seznam se liší podle
> konkrétní třídy — závisí na tom, co je deklarované v `_inners`. Tahle
> tabulka popisuje *mechanismus* (že každý inner dostane dvojici
> property/instance property), ne konkrétní jména, která jsou vždy
> specifická pro danou kompozici.

[▲ Nahoru](#-obsah)

---

## 4. Kompozitní immutable instance

Vytvoří se voláním `MyObject(mutable=False)`. Dědí **vše** z
[atomické immutable instance](#2-atomická-immutable-instance) plus
strukturu z [kompozitní mutable varianty](#3-kompozitní-mutable-instance),
minus reaktivní zapisovací mechanismy.

### Rozdíly oproti kompozitní mutable variantě

| Člen | Rozdíl |
|---|---|
| `value` | Jen getter — stejně jako u atomické immutable varianty. |
| `<jméno_inner>` | Jen getter — zápis do žádného vnitřního prvku není povolený. |
| `_recalculate_self` | **Neexistuje.** Přidává se do `class_dict` jen podmíněně, `if mutable`. |
| `_recalculate_inners` | **Neexistuje.** Stejný důvod. |

`<jméno_inner>_instance` zůstává (je vždy jen ke čtení, bez ohledu na
mutabilitu) a `calculate_value`/`decompose_value` zůstávají dostupné jako
zděděné metody — jde jen o výpočet/rozklad, ne o mutaci stavu instance.

Immutable kompozice je tedy po vytvoření **strukturálně zmrazená** — hodnotu
lze přečíst na libovolné úrovni stromu, ale nikde ji nelze změnit.

[▲ Nahoru](#-obsah)
