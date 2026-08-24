# 🔒 `with_any` — Univerzální immutabilní aktualizace

Nejvyšší vrstva immutabilního update pipeline — jediný vstupní bod, který
zvládne **libovolnou** kombinaci změn (jednu konstantu, jednu kompozici,
dávku konstant, dávku kompozic, nebo cokoliv smíchané dohromady) a sám
si rozmyslí, v jakém pořadí a jak to bezpečně aplikovat. Staví na všech
třech předchozích dokumentech —
[`with_constant`](README_WITH_CONSTANT.md),
[`with_constants`](README_WITH_CONSTANTS.md),
[`with_composite`](README_WITH_COMPOSITE.md) — a přidává vrstvu, která
mezi nimi inteligentně směruje.

> Stejný integrační požadavek jako u předchozích funkcí: instance musí
> dědit ze `Snapshot` a `NodesDicts`.

```
with_any
├── split_changes            (rozdělí vstup na konstanty / kompozice)
├── get_top_composite_paths  (najde "kořenové" kompozitní změny)
├── with_composite           (aplikuje kořenové kompozice)
├── split_constants_paths    (rozdělí konstanty na "obsažené" / "unikátní")
├── with_constants           (aplikuje unikátní konstanty)
└── process_single_change    (zkratka pro jednu jedinou změnu)
```

---

## 🧭 Obsah

* [`with_any` — hlavní pipeline](#with_any--hlavní-pipeline)
* [`process_single_change` — zkratka pro jednu změnu](#process_single_change--zkratka-pro-jednu-změnu)
* [`split_changes` — konstanty vs. kompozice](#split_changes--konstanty-vs-kompozice)
* [`get_top_composite_paths` — kořenové vs. vnořené kompozice](#get_top_composite_paths--kořenové-vs-vnořené-kompozice)
* [`split_constants_paths` — obsažené vs. unikátní konstanty](#split_constants_paths--obsažené-vs-unikátní-konstanty)
* [Proč je potřeba tahle celá orchestrace](#proč-je-potřeba-tahle-celá-orchestrace)

---

## `with_any` — hlavní pipeline

**Parametry:** `self`, `changes` (`ChangeTuple | ChangesTuple | None`).

**Návratová hodnota:** nová instance (immutable mód), nebo přímo hodnota
(`instance.value`, pokud `self.__is_mutable__` — viz poznámka níže).

**Třináct kroků, ale dají se shrnout do čtyř fází:**

```
FÁZE A — triviální cesty (kroky 1–3)
  1. changes je prázdné/None → vytvoř kopii beze změny
  2. changes musí být tuple
  3. jediná změna (ne tuple tuplů) → deleguj na process_single_change

FÁZE B — klasifikace (kroky 4–7)
  4. split_changes → (constants, composite)
  5. jen konstanty → deleguj rovnou na with_constants
  6. postav changes_dict pro rychlý přístup podle jména
  7. get_top_composite_paths → (top_composite, child_composite)

FÁZE C — aplikace kompozic shora dolů (kroky 8–11)
  8. vytvoř čerstvou instanci (kopii) jako pracovní základ
  9. pro každé jméno v top_composite: instance = with_composite(instance, name, ...)
  10. sejmi snapshot_dict z instance PO aplikaci kompozic
  11. ověř, že child_composite hodnoty souhlasí s tím, co už kompozice nastavila

FÁZE D — aplikace konstant (kroky 12–13)
  12. split_constants_paths → (contained, unique); ověř contained; aplikuj unique
  13. vrať instance (nebo instance.value, pokud self.__is_mutable__)
```

**Fáze A: proč existují tři různé "výstupy" pro triviální vstupy?**
Kroky 1 a 3 nejsou jen optimalizace — jsou to **různé sémantiky**. Krok 1
(`not changes`) znamená "žádná změna, jen mi vrať ekvivalentní novou
instanci" (užitečné třeba jako explicitní "klon"). Krok 3 (jediná změna)
deleguje na specializovanou, jednodušší [`process_single_change`](#process_single_change--zkratka-pro-jednu-změnu) —
zbytečné by bylo pouštět celou těžkotonážní klasifikační mašinerii kroků
4–13 jen kvůli jedné jediné položce.

**Fáze B, krok 5 — "jen konstanty" je další zkratka.** Pokud po
`split_changes` vyjde, že žádná ze změn není kompozitní, celá zbylá
komplikovaná orchestrace (fáze C a D) je zbytečná — `with_constants`
(viz [README_WITH_CONSTANTS.md](README_WITH_CONSTANTS.md)) už sama umí
efektivně zpracovat dávku samotných konstant, včetně optimalizovaného
přepočtu jen z nejhlubších míst.

**Fáze C je jádro celé složitosti `with_any` — a důvod, proč existuje.**
Kompozitní změny se musí aplikovat **od kořene směrem dolů** (`top_composite`
napřed), protože aplikace kořenové kompozice (přes `with_composite` →
`reacalculate_inners`) **sama** nastaví hodnoty všech svých vnořených
prvků. Pokud uživatel zároveň žádal změnu i na některém z těch vnořených
prvků (`child_composite`), nejde tuhle druhou změnu **aplikovat znovu** —
to by bylo nekonzistentní (dvě různé cesty, jak dojít ke stejné hodnotě,
mohou dát různý výsledek). Místo aplikace se tedy `child_composite`
změny jen **ověří** (krok 11) proti tomu, co už nastavila kořenová
kompozice — pokud uživatel zadal hodnotu, která **neodpovídá** tomu, co
by vyplynulo z kořenové změny, je to `raise_with_any_child_composite_mismatch`.

**Fáze D, krok 12 řeší analogický problém pro konstanty** —
[`split_constants_paths`](#split_constants_paths--obsažené-vs-unikátní-konstanty)
rozliší konstanty, které **leží uvnitř** už aplikované kořenové kompozice
(ty se jen ověří, ne znovu aplikují — ze stejného důvodu jako
`child_composite` výše), od konstant, které jsou na cestě **mimo**
jakoukoliv aplikovanou kompozici (ty se skutečně aplikují, přes
`with_constants`).

**`self.__is_mutable__` na konci není chyba — je to záměrná duální
sémantika.** `with_any` (a celý immutabilní subsystém) se typicky volá
i z mutable instancí (např. jako implementace nějaké veřejné "copy-with"
metody) — v tom případě dává smysl vrátit rovnou **hodnotu**
(`instance.value`), ne celou immutable instanci, protože volající
pracuje v mutable kontextu a immutable instance by tam byla cizí
koncept.

[▲ Nahoru](#-obsah)

---

## `process_single_change` — zkratka pro jednu změnu

**Parametry:** `self`, `change` (jeden `(jméno, hodnota)` pár).

**Návratová hodnota:** nová instance.

```python
def process_single_change(self, change):
    # validace struktury (jméno, hodnota)
    name, value = change

    if name in self._constant_names_set:
        return with_constant(self, name, value)

    if name in self.meta.node_names_set:
        return with_composite(self, name, value)

    raise_with_any_unknown_name(self, name, value)
```

**Nejmenší směrovací jednotka v celém subsystému** — jen dvě podmínky,
žádná klasifikace do skupin, žádné hledání kořenových cest. Existuje
čistě proto, aby `with_any` nemusel pro jedinou změnu spouštět celou
těžkou mašinerii `split_changes`/`get_top_composite_paths` — přímočará
delegace na `with_constant`, nebo `with_composite`, podle toho, kam
`name` patří.

[▲ Nahoru](#-obsah)

---

## `split_changes` — konstanty vs. kompozice

**Parametry:** `self`, `changes` (tuple párů).

**Návratová hodnota:** `tuple[ChangesTuple, ChangesTuple]` — `(constants,
composite)`.

```python
def split_changes(self, changes):
    constants, composite = [], []
    for inner_tuple in changes:
        # validace struktury (jméno, hodnota)
        name = inner_tuple[0]

        if name in self._constant_names_set:
            constants.append(inner_tuple)
        elif name in self.meta.node_names_set:
            composite.append(inner_tuple)
        else:
            raise_split_changes_unknown_name(self, name)

    return tuple(constants), tuple(composite)
```

**První, nejzákladnější třídicí krok celé `with_any` pipeline** — jen
rozhodne, do které ze dvou skupin patří každá jednotlivá změna. Dvě
množiny (`self._constant_names_set` a `self.meta.node_names_set`, obě
zděděné z [`NodesTuple`](../core_mixins)/metadat) jsou **kanonický zdroj
pravdy** pro tohle rozhodnutí — žádná heuristika, žádné hádání podle
typu hodnoty. Jméno, které neodpovídá ani jedné množině, je okamžitě
neplatný vstup (`raise_split_changes_unknown_name`) — fail-fast, dřív než
se s ním pipeline vůbec pokusí pracovat dál.

[▲ Nahoru](#-obsah)

---

## `get_top_composite_paths` — kořenové vs. vnořené kompozice

**Parametry:** `composite` (tuple `(jméno, hodnota)` párů, jen kompozice),
`nodes_path_dict`.

**Návratová hodnota:** `tuple[PathDict, PathDict]` — `(top_composite,
child_composite)`.

```python
def get_top_composite_paths(composite, nodes_path_dict):
    top_composite, top_composite_paths, child_composite = {}, [], {}

    sorted_paths = sorted(
        ((name, nodes_path_dict[name]) for name, _ in composite),
        key=lambda item: len(item[1]),
    )

    for key, path in sorted_paths:
        if not any(path[:len(parent)] == parent for parent in top_composite_paths):
            top_composite[key] = path
            top_composite_paths.append(path)
        else:
            child_composite[key] = path

    return top_composite, child_composite
```

**Řazení podle délky cesty (`len(item[1])`), ne lexikograficky.** Tohle
je jiné kritérium než u [`find_longest_keys`](README_WITH_CONSTANTS.md#find_longest_keys--proč-je-potřeba)
(která řadí podle obsahu cesty) — tady jde o to najít **nejkratší**
(nejvýše položené) cesty jako první, protože se prochází **shora dolů**:
jakmile je jednou nějaká cesta uznaná jako "kořenová" (`top_composite`),
zapíše se do `top_composite_paths` a **všechny další** cesty, které pod
ni spadají (test `path[:len(parent)] == parent`, tedy prefix shoda),
jsou automaticky `child_composite` — bez ohledu na to, jak hluboko
zanořené jsou. Krátké cesty se tedy musí zpracovat **dřív**, aby mohly
sloužit jako "filtr" pro delší cesty, které přijdou po nich.

**Výsledek `top_composite` je přesně množina, kterou `with_any` krok 9
aplikuje** — a protože se `child_composite` cesty nikdy neaplikují
znovu (jen ověřují, viz výše), je tenhle krok tím, co zaručuje, že se
žádná kompozitní změna neaplikuje **dvakrát** ani **v nesprávném pořadí**
(dítě před rodičem by mohlo vést k tomu, že rodičovská aplikace dítě
zase přepíše).

[▲ Nahoru](#-obsah)

---

## `split_constants_paths` — obsažené vs. unikátní konstanty

**Parametry:** `constants` (tuple `(jméno, hodnota)` párů), `used_paths_dict`
(cesty už aplikovaných kořenových kompozic), `nodes_path_dict`.

**Návratová hodnota:** `tuple[PathDict, PathDict]` — `(contained, unique)`.

```python
def split_constants_paths(constants, used_paths_dict, nodes_path_dict):
    constants_paths = {name: nodes_path_dict[name] for name, _ in constants}

    root_prefixes = [
        path[:-1] if path and path[-1] == "_value" else path
        for path in used_paths_dict.values()
    ]

    contained, unique = {}, {}
    for key, path in constants_paths.items():
        if any(path[:len(prefix)] == prefix for prefix in root_prefixes):
            contained[key] = path
        else:
            unique[key] = path

    return contained, unique
```

**Normalizace `root_prefixes` (odseknutí koncového `"_value"`) je
klíčový detail, kterým se aktuální verze liší od staršího řešení.**
Cesty kompozitních uzlů typicky končí segmentem `_value` (odkazujícím na
jejich vlastní hodnotový slot) — ale cesty jejich **vnitřních prvků**
tenhle segment nemají, protože jsou to samostatné pod-cesty ve stromu.
Kdyby se porovnávalo bez odseknutí, prefix test (`path[:len(prefix)] ==
prefix`) by nikdy nenašel shodu mezi cestou konstanty a "surovou" cestou
kompozice končící na `_value` — proto se `_value` napřed odstraní, aby
`root_prefixes` reprezentovaly čistě **strukturální větev** stromu, ne
konkrétní hodnotový uzel na jejím konci. Tahle oprava je přesně to, co
umožňuje, aby prefix test v hlavní smyčce fungoval spolehlivě pro
libovolnou hloubku zanoření.

**Stejný "prefix" princip jako u `get_top_composite_paths`, ale tady v
opačném směru** — místo hledání "kdo je kořen" mezi navzájem podobnými
kompozitními cestami, tahle funkce hledá "spadá tahle konstanta pod
už-aplikovanou kompozici, nebo ne". `contained` (spadá) se v `with_any`
kroku 12 jen **ověří** proti tomu, co kompozice už nastavila; `unique`
(nespadá) se skutečně **aplikuje** přes `with_constants`.

[▲ Nahoru](#-obsah)

---

## Proč je potřeba tahle celá orchestrace

Celý smysl `with_any` (a jeho čtyř pomocných funkcí) je jedna věta:
**zabránit tomu, aby se stejná logická změna aplikovala dvakrát, nebo v
nesprávném pořadí**, když uživatel zadá mix změn na různých úrovních
stromu najednou. Bez týhle orchestrace by bylo snadné omylem:

* aplikovat kompozitní změnu, a pak **znovu** (nekonzistentně)
  přepsat jeden z jejích vnitřních prvků přímou hodnotou,
* aplikovat vnořenou kompozici **před** její rodičovskou kompozicí, což
  by rodičovská aplikace stejně přepsala,
* zbytečně opakovaně přepočítávat sdílené rodiče (řeší
  [`find_longest_keys`](README_WITH_CONSTANTS.md#find_longest_keys--proč-je-potřeba)
  uvnitř `with_constants`, na kterou `with_any` deleguje).

Výsledkem je, že `with_any(self, spousta_různých_změn)` dá **vždy stejný,
deterministický výsledek**, bez ohledu na to, v jakém pořadí uživatel
změny v tuple napsal — protože skutečné pořadí aplikace (shora dolů,
kompozice před ověřením konstant) řídí interní klasifikace, ne pořadí
vstupu.

[▲ Nahoru](#-obsah)
