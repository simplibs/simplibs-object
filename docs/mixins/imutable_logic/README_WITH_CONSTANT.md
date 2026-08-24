# 🔒 `with_constant` — Immutabilní aktualizace jedné konstanty

Tenhle dokument popisuje nejmenší stavební kámen celého immutabilního
update pipeline — funkci, která bezpečně změní **jednu** konstantu na
immutable instanci, aniž by ji mutovala: vytvoří **novou** instanci se
správně přepočítanou strukturou. Na `with_constant` (a hlavně na jeho
utility) staví `with_constants`, `with_composite` i `with_any`.

> **Integrační požadavek:** instance, na které se tyhle funkce volají,
> musí dědit z `Snapshot` (poskytuje `_restore_snapshot`) a `NodesDicts`
> (poskytuje `_nodes_dict`, `_nodes_tuple`...). Bez nich pipeline spadne
> na `AttributeError`.

```
with_constant
├── create_snapshot_dict     (aktuální stav → plochý dict)
├── reacalculate_owner_value (přepočet kompozitních rodičů)
└── create_new_instance      (materializace nové instance)  ← používá se i samostatně
```

---

## 🧭 Obsah

* [`with_constant` — hlavní pipeline](#with_constant--hlavní-pipeline)
* [`create_snapshot_dict` — plochá pracovní kopie stavu](#create_snapshot_dict--plochá-pracovní-kopie-stavu)
* [`reacalculate_owner_value` — přepočet směrem k rootu](#reacalculate_owner_value--přepočet-směrem-k-rootu)
* [`create_new_instance` — materializace (používá se samostatně)](#create_new_instance--materializace-používá-se-samostatně)

---

## `with_constant` — hlavní pipeline

**Parametry:** `self` (instance s `Snapshot`+`NodesDicts`), `name` (jméno
konstanty), `new_value`.

**Návratová hodnota:** nová instance se změněnou hodnotou.

**Sedm kroků:**

```python
def with_constant(self, name, new_value):
    if name not in self._constant_names_set:
        raise_immutability_constant_not_found(self, name)

    instance, path = self._nodes_dict[name]
    instance.validate(new_value)

    snapshot_dict = create_snapshot_dict(self._nodes_tuple)
    snapshot_dict[name] = new_value

    reacalculate_owner_value(snapshot_dict, instance.owner)

    new_snapshot = tuple(snapshot_dict.values())
    return create_new_instance(self, new_snapshot)
```

**Proč `name` musí být konstanta, ne libovolný uzel.** Kontrola `name not
in self._constant_names_set` hned na začátku zajišťuje, že `with_constant`
neomylem "neuvidí" kompozitní uzel — to je vyhrazené pro
[`with_composite`](README_WITH_COMPOSITE.md), který navíc musí řešit
propagaci **dolů** do vnitřních prvků (co `with_constant` řešit nemusí,
protože konstanta žádné vnitřní prvky nemá).

**Validace proběhne dřív, než se cokoliv zapíše** — `instance.validate(new_value)`
je druhý krok, ještě před vytvořením snapshot slovníku. Neplatná hodnota
se tedy odhalí, aniž by se vůbec začal budovat žádný mezistav.

**Sedm kroků odpovídá přesně sekvenci "over → write → recalc → materialize"**:
zjisti si cíl (`_nodes_dict[name]`), zvaliduj, udělej plochou pracovní
kopii (`create_snapshot_dict`), zapiš novou hodnotu do kopie, přepočítej
rodiče (`reacalculate_owner_value`), sestav finální pozicovaný tuple, a
nakonec z něj postav novou instanci (`create_new_instance`). Tenhle
pětiprvkový vzor "sejmi snapshot → uprav dict → přepočítej → tuple →
nová instance" se opakuje ve všech ostatních `with_*` funkcích téměř
identicky — jen se liší to, **co přesně** se do slovníku zapíše a jak
komplikovaný je přepočet.

[▲ Nahoru](#-obsah)

---

## `create_snapshot_dict` — plochá pracovní kopie stavu

**Parametry:** `nodes_tuple` (z `NodesTuple` mixinu, viz
[NodesTuple design notes](#poznámka-k-nodestuple-nodesdicts-snapshot) níže).

**Návratová hodnota:** `dict[str, Any]` — `{name_snake: _value}`.

```python
def create_snapshot_dict(nodes_tuple):
    return {
        instance.meta.name_snake: instance._value
        for instance, _ in nodes_tuple
    }
```

**Proč `dict`, když `Snapshot` mixin používá tuple?** `Snapshot._build_snapshot()`
(viz `Snapshot.py`) vrací poziční `tuple` hodnot — kompaktní, ale
nepohodlný pro **cílené** úpravy (chceš změnit jen jednu konkrétní
hodnotu podle jména, ne přepočítávat celou pozici v tuple ručně).
`create_snapshot_dict` je most mezi oběma světy: převede `_nodes_tuple`
na dict klíčovaný podle `name_snake`, který jde snadno mutovat na
jednom konkrétním klíči, a na konci pipeline (`tuple(snapshot_dict.values())`)
se zase převede zpátky na poziční tuple — protože `_restore_snapshot`
(volaná uvnitř `create_new_instance`) očekává právě tenhle formát.

**Je to čistě pracovní mezistav, ne trvalá struktura** — vzniká na
začátku pipeline, mutuje se v jejím průběhu, a na konci se zahodí (poté,
co se z něj vytáhne finální `tuple(...)`).

[▲ Nahoru](#-obsah)

---

## `reacalculate_owner_value` — přepočet směrem k rootu

**Parametry:** `snapshot_dict` (mutovaný na místě), `owner` (instance,
odkud se začíná — typicky přímý rodič změněného uzlu).

**Návratová hodnota:** `None` — mutuje `snapshot_dict` na místě.

```python
def reacalculate_owner_value(snapshot_dict, owner):
    current_owner = owner
    while current_owner is not UNSET:
        owner_inners_name = (inner.meta.name_snake for inner in current_owner.meta.inners)
        owner_inners_value_dict = {name: snapshot_dict[name] for name in owner_inners_name}

        new_value = current_owner.meta.logic(**owner_inners_value_dict)
        snapshot_dict[current_owner.meta.name_snake] = new_value

        current_owner = current_owner.owner
```

**Iterativní výstup po `_owner` řetězu, ne rekurze.** `while current_owner
is not UNSET` postupně stoupá od bezprostředního rodiče až ke kořeni
celého stromu — `UNSET` je hodnota `_owner` na kořenové instanci (viz
[README_ATOM_CLASS.md](README_ATOM_CLASS.md#create_atom_init--konstruktor)),
takže smyčka přirozeně skončí, jakmile dojde na vrchol.

**Přímé volání `current_owner.meta.logic(...)`, ne `calculate_value`.**
Všimni si, že se **neprochází** přes veřejné `calculate_value`
(porovnej s [README_SIMPLE_OBJECT.md](README_SIMPLE_OBJECT.md#calculate_value)) —
volá se rovnou surová `_logic` funkce z metadat. Design notes to
zdůvodňují přímo: hodnoty ve `snapshot_dict` jsou **už jednou validované**
(prošly `instance.validate(new_value)` v `with_constant`, nebo jsou to
prostě nezměněné, dříve platné hodnoty), takže by bylo zbytečné je
znovu validovat a zpracovávat přes `_process_calculate_value_params` —
tohle je vědomá optimalizace pro interní, důvěryhodnou cestu dat.

**Tohle je jediný směr reaktivity, který immutabilní pipeline potřebuje
řešit ručně.** U mutable instancí tohle dělá automaticky `_recalculate_self`
(viz [README_COMPOSITE_CLASS.md](README_COMPOSITE_CLASS.md#create_recalculate_self--tok-hodnot-nahoru))
jako vedlejší efekt zápisu do slotu. Immutable instance ale žádný zápis
nepovoluje (viz
[README_VALUE_PROPERTIES.md](README_VALUE_PROPERTIES.md#create_value_property--sestavení-property)) —
proto musí `reacalculate_owner_value` udělat **ručně, v předstihu**,
ještě než vůbec vznikne nová instance, přesně tu samou práci, kterou by
jinak odvedl reaktivní mechanismus za běhu.

[▲ Nahoru](#-obsah)

---

## `create_new_instance` — materializace (používá se samostatně)

**Parametry:** `instance` (šablona — odkud se vezme třída), `snapshot`
(poziční tuple hodnot).

**Návratová hodnota:** nová, plně inicializovaná instance stejné třídy.

```python
def create_new_instance(instance, snapshot):
    new_instance = object.__new__(type(instance))
    new_instance.__init__()
    new_instance._restore_snapshot(snapshot)
    return new_instance
```

**Tři kroky, každý s jasným důvodem:**

1. **`object.__new__(type(instance))`** — obchází `SimpleMeta.__call__`
   úplně stejným způsobem, jaký znáš z
   [`create_composite_init`](README_COMPOSITE_CLASS.md#create_composite_init--konstruktor) —
   `type(instance)` je totiž už hotová, zkompilovaná runtime třída
   (`_is_instance_class = True`), ne blueprint, takže by procházení přes
   metaclass bylo zbytečné a nesprávné.
2. **`new_instance.__init__()`** — spustí **celou** standardní
   inicializační sekvenci (sloty, `init_mixins`, u kompozic i vytvoření
   vnitřních prvků) — nová instance tak vznikne stejně "kompletní" jako
   kterákoliv jiná, jen zatím s výchozími hodnotami.
3. **`_restore_snapshot(snapshot)`** — teprve teď se do ní "vlije" skutečný
   stav ze snapshotu (metoda pochází z mixinu `Snapshot`) — přímý zápis
   do `instance._value` na každém uzlu, mimo běžný setter/validaci,
   protože hodnoty v `snapshot` už jsou důvěryhodné (buď prošly validací
   dřív v pipeline, nebo jsou to nezměněné, dříve platné hodnoty).

**Proč má tahle funkce "zvláštní pozici", jak zmiňuješ.** I když vznikla
jako pomocná utilita pro `with_constant`, je natolik obecná (šablona +
snapshot → hotová instance), že ji **přímo** volají i `with_constants`,
`with_composite` i `with_any` (viz
[README_WITH_ANY.md](README_WITH_ANY.md)) — vždy jako **poslední krok**
jejich vlastní pipeline, bez ohledu na to, jak složitá byla cesta k
finálnímu `snapshot` tuple. Je to jediné místo v celém immutabilním
subsystému, kde skutečně vzniká nová instance — všechno ostatní jen
připravuje data pro tenhle jeden okamžik.

[▲ Nahoru](#-obsah)

➡️ Pokračování: [README_WITH_CONSTANTS.md](README_WITH_CONSTANTS.md)
