# 🔒 `with_composite` — Immutabilní aktualizace kompozitního uzlu

Strukturální protějšek [`with_constant`](README_WITH_CONSTANT.md) —
řeší situaci, kdy se mění hodnota **kompozitního** uzlu (ne listové
konstanty). Na rozdíl od konstanty musí zvládnout přepočet
**oběma směry**: dolů do vnitřních prvků (dekompozicí) i nahoru k
rodičovským kompozicím.

> Stejný integrační požadavek jako u `with_constant`: instance musí dědit
> ze `Snapshot` a `NodesDicts`.

```
with_composite
├── with_constant             (delegace, pokud je name ve skutečnosti konstanta)
├── create_snapshot_dict      (sdílené s with_constant)
├── reacalculate_inners       (nový: propagace DOLŮ)
├── reacalculate_owner_value  (sdílené s with_constant: propagace NAHORU)
└── create_new_instance       (sdílené s with_constant)
```

---

## 🧭 Obsah

* [`with_composite` — hlavní pipeline](#with_composite--hlavní-pipeline)
* [`reacalculate_inners` — přepočet směrem dolů](#reacalculate_inners--přepočet-směrem-dolů)

---

## `with_composite` — hlavní pipeline

**Parametry:** `self`, `name` (jméno kompozitního uzlu), `new_value`.

**Návratová hodnota:** nová instance.

**Devět kroků:**

```python
def with_composite(self, name, new_value):
    if name in self._constant_names_set:
        return with_constant(self, name, new_value)      # 1. delegace

    if name not in self.meta.node_names_set or not self.meta.is_decomposeable:
        validate_composite_name_exists(self, name)         # 2. validace existence + dekomponovatelnosti
        validate_composite_is_decomposeable(self, name)

    instance, path = self._nodes_dict[name]
    instance.validate(new_value)                            # 3. validace hodnoty

    snapshot_dict = create_snapshot_dict(self._nodes_tuple)  # 4.
    snapshot_dict[name] = new_value                          # 5.

    reacalculate_inners(snapshot_dict, instance.meta, new_value)   # 6. DOLŮ
    reacalculate_owner_value(snapshot_dict, instance.owner)        # 7. NAHORU

    new_snapshot = tuple(snapshot_dict.values())              # 8.
    return create_new_instance(self, new_snapshot)             # 9.
```

**Krok 1 — delegace na `with_constant` je vědomá, uživatelsky přívětivá
zkratka.** `with_composite` sama o sobě neví (a nemusí vědět) předem,
jestli `name` odkazuje na konstantu, nebo na kompozici — prostě to
zkontroluje a pokud jde o konstantu, celou zbytek logiky přeskočí a
deleguje na specializovanou, jednodušší funkci. Tohle umožňuje, aby
vyšší vrstvy (`with_any`, viz [README_WITH_ANY.md](README_WITH_ANY.md))
nemusely samy řešit tohle rozlišení všude, kde by se `with_composite`
mohlo hodit volat.

**Dvě nezávislé fáze přepočtu — dolů (krok 6) a nahoru (krok 7) — v
tomhle přesném pořadí.** Tohle je klíčový architektonický rozdíl oproti
`with_constant`, který řeší jen jeden směr (nahoru). Kompozitní uzel
totiž **má** vnitřní prvky, které musí zůstat konzistentní s novou
hodnotou (proto krok 6, `reacalculate_inners`), a zároveň může **sám**
být vnitřním prvkem něčeho výš (proto krok 7, stejná
`reacalculate_owner_value` jako u `with_constant`). Pořadí "dolů, pak
nahoru" dává smysl — `reacalculate_inners` pracuje jen s podstromem pod
`name` a nezávisí na ničem nad ním, zatímco `reacalculate_owner_value`
čte z `snapshot_dict` hodnoty (včetně těch, co právě zapsal krok 6, pokud
by na ně nějaký předek přímo odkazoval), takže musí běžet až po něm.

[▲ Nahoru](#-obsah)

---

## `reacalculate_inners` — přepočet směrem dolů

**Parametry:** `snapshot_dict` (mutovaný na místě), `meta` (metadata
kompozitního uzlu, jehož hodnota se právě změnila), `new_value`.

**Návratová hodnota:** `None`.

```python
def reacalculate_inners(snapshot_dict, meta, new_value):
    inners_meta = (inner.meta for inner in meta.inners)
    inners_value = meta.decompose(new_value)

    for inner_meta, inner_value in zip(inners_meta, inners_value):
        snapshot_dict[inner_meta.name_snake] = inner_value

        if not inner_meta.is_constant:
            reacalculate_inners(snapshot_dict, inner_meta, inner_value)
```

**Rekurzivní, na rozdíl od `reacalculate_owner_value` (která je
iterativní).** Tenhle rozdíl má strukturální důvod: cesta **nahoru** je
vždy lineární (jeden uzel má vždy nejvýš jednoho `_owner`, takže `while`
smyčka stačí), zatímco cesta **dolů** se **větví** (jeden kompozitní uzel
může mít víc `_inners`, z nichž každý může mít další vnořené `_inners`) —
takže přirozeně vyžaduje rekurzi, ne jednoduchou smyčku.

**Používá `meta.decompose(new_value)` přímo, stejný vzor "surové
metadatové volání" jako `reacalculate_owner_value` používá `meta.logic(...)`**
(viz [README_WITH_CONSTANT.md](README_WITH_CONSTANT.md#reacalculate_owner_value--přepočet-směrem-k-rootu)) —
obchází veřejné `decompose_value` (porovnej s
[README_SIMPLE_OBJECT.md](README_SIMPLE_OBJECT.md#decompose_value)), protože
`new_value` už v tomhle bodě pipeline prošla validací (`instance.validate(new_value)`
v `with_composite`), takže druhá validace by byla zbytečná.

**Podmínka `if not inner_meta.is_constant` je to, co dělá rekurzi
konečnou i pro libovolně hluboké stromy.** Pokud je vnitřní prvek atom
(`is_constant`), rekurze se pro něj nespustí — atom nemá co dál
dekomponovat. Pokud je to další kompozice, funkce se zavolá znovu, se
`snapshot_dict` (sdíleným, mutovaným napříč celou rekurzí) a novými
`inner_meta`/`inner_value` — takže se stejný mechanismus propaguje do
libovolné hloubky vnořených kompozic, přesně jako
[`_recalculate_inners`](README_COMPOSITE_CLASS.md#create_recalculate_inners--tok-hodnot-dolů)
dělá pro mutable instance, jen tady pracuje nad `snapshot_dict` místo
přímo nad sloty instance.

[▲ Nahoru](#-obsah)

➡️ Pokračování: [README_WITH_ANY.md](README_WITH_ANY.md)
