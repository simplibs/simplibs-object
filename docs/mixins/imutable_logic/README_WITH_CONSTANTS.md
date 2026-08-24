# 🔒 `with_constants` — Dávková immutabilní aktualizace konstant

Dávková varianta [`with_constant`](README_WITH_CONSTANT.md) — místo
jedné konstanty najednou umí bezpečně změnit **libovolný počet** konstant
v jediném kroku, s **jedním** finálním přepočtem struktury místo
opakovaného přepočítávání po každé jednotlivé změně.

> Stejný integrační požadavek jako u `with_constant`: instance musí dědit
> ze `Snapshot` a `NodesDicts`.

```
with_constants
├── create_snapshot_dict     (ze with_constant/utils, sdílené)
├── find_longest_keys        (najde "nejhlubší" změněné uzly)
├── reacalculate_owner_value (spuštěné z každého nejhlubšího uzlu)
└── create_new_instance      (sdílené s with_constant)
```

---

## 🧭 Obsah

* [`with_constants` — hlavní pipeline](#with_constants--hlavní-pipeline)
* [`find_longest_keys` — proč je potřeba](#find_longest_keys--proč-je-potřeba)

---

## `with_constants` — hlavní pipeline

**Parametry:** `self`, `changes` (`ChangeTuple | ChangesTuple | None`) —
buď jeden pár `(jméno, hodnota)`, nebo tuple takových párů.

**Návratová hodnota:** nová instance se všemi změnami aplikovanými najednou.

**Šest kroků:**

```
1. snapshot_dict = create_snapshot_dict(self._nodes_tuple)
2. path_dict = {}
3. new_snapshot = self._build_snapshot()   ← fallback, pokud changes je prázdné

4. (jen pokud changes existují)
   4.1 changes MUSÍ být tuple
   4.2 normalizace: jeden pár (jméno, hodnota) → obalí se do tuple párů
   4.3 pro každý (jméno, hodnota):
       - validace struktury páru
       - jméno MUSÍ být v self._constant_names_set
       - validace hodnoty přes instance.validate
       - zápis do snapshot_dict
       - zápis cesty do path_dict
   4.4 longest_key = find_longest_keys(path_dict)
   4.5 pro každý klíč v longest_key: reacalculate_owner_value(...)
   4.6 new_snapshot = tuple(snapshot_dict.values())

5. return create_new_instance(self, new_snapshot)
```

**Normalizace jednoho páru na tuple párů** (krok 4.2, `if not
isinstance(changes[0], tuple): changes = (changes,)`) — stejný vzor
pohodlnosti jako `assert_mixins_slots_values` (viz
[README_MIXIN_TESTING.md](README_MIXIN_TESTING.md#assert_mixins_slots_values--kontrola-hodnot-slotů)):
`with_constants(self, ("age", 25))` a `with_constants(self, (("age",
25),))` fungují identicky, takže uživatel nemusí u jediné změny psát
zbytečně vnořený tuple.

**Klíčový rozdíl oproti opakovanému volání `with_constant`** je ve
**fázi přepočtu** (kroky 4.4–4.5). Kdybys místo `with_constants` zavolal
`with_constant` desetkrát za sebou, každé volání by nezávisle přepočítalo
celou cestu ke kořeni — u sdílených rodičů by to znamenalo **opakovanou,
zbytečnou práci** (stejný kompozitní uzel přepočítaný vícekrát). `with_constants`
tomu předchází tak, že napřed **sesbírá všechny změny** do jednoho
`snapshot_dict`, a teprve pak spustí přepočet — jen z **nejhlubších**
změněných míst (viz `find_longest_keys` níže), takže každý sdílený rodič
se přepočítá **právě jednou**, bez ohledu na to, kolik jeho potomků se
změnilo.

[▲ Nahoru](#-obsah)

---

## `find_longest_keys` — proč je potřeba

**Parametry:** `path_dict` (`{jméno: cesta}` pro každou změněnou konstantu).

**Návratová hodnota:** `tuple[str, ...]` — jména jen těch konstant, jejichž
cesta je "terminální" (nejhlubší) mezi zadanými.

```python
def find_longest_keys(path_dict):
    sorted_path = sorted(path_dict.items(), key=lambda x: x[1])
    longest_keys = []

    for i in range(len(sorted_path) - 1):
        key, path = sorted_path[i]
        _, next_path = sorted_path[i + 1]
        if next_path[:len(path)] == path:
            continue  # path je prefix next_path → NENÍ terminální
        longest_keys.append(key)

    longest_keys.append(sorted_path[-1][0])  # poslední je vždy terminální
    return tuple(longest_keys)
```

**Proč by bylo špatně spustit přepočet ze všech změněných uzlů rovnou.**
Představ si kompozici `Car` s vnitřním `Engine`, který má vnitřní
`Cylinder`. Pokud uživatel změní `cylinder_count` i `engine_power` (kde
`engine_power` je *přímo* na `Engine`, ne na `Cylinder`), obě cesty vedou
ke stejnému rodiči (`Engine`) — kdyby se `reacalculate_owner_value`
spustilo z **obou** míst nezávisle, `Engine` (a `Car` nad ním) by se
přepočítal **dvakrát**. `find_longest_keys` tenhle problém řeší tak, že
identifikuje jen ty změny, které jsou skutečně na "listové", nejhlubší
úrovni vůči **ostatním zadaným změnám** — a `reacalculate_owner_value`
(které stejně stoupá až ke kořeni, viz
[README_WITH_CONSTANT.md](README_WITH_CONSTANT.md#reacalculate_owner_value--přepočet-směrem-k-rootu))
se pak spustí jen z těchhle míst, čímž automaticky pokryje i všechny
mezilehlé úrovně, aniž by je počítalo víckrát.

**Algoritmus je založený na řazení cest a testu prefixu, ne na
explicitním porovnávání stromu.** `sorted(path_dict.items(), key=lambda
x: x[1])` seřadí položky podle jejich cesty (tuple řetězců, které se
porovnávají lexikograficky prvek po prvku) — díky tomu, pokud je cesta A
předkem cesty B, po seřazení bude A bezprostředně **před** B (nebo někde
před ní ve skupině sourozeneckých cest se stejným prefixem). Test `next_path[:len(path)]
== path` pak jen ověří, jestli je aktuální cesta **prefixem** té
následující v seřazeném pořadí — pokud ano, aktuální cesta je "rodič",
který **není** potřeba zahrnout (jeho zpracování by bylo redundantní vůči
zpracování jeho potomka). Poslední prvek seřazeného seznamu je vždy
zahrnutý bezpodmínečně, protože žádný jiný prvek nemůže být jeho
následníkem k porovnání.

[▲ Nahoru](#-obsah)

➡️ Pokračování: [README_WITH_COMPOSITE.md](README_WITH_COMPOSITE.md)
