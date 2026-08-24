# 🧪 Testování objektů a konstant — `assert_simple_object`

Zatímco [README_MIXIN_TESTING.md](README_MIXIN_TESTING.md) testuje mixiny
samotné, tenhle dokument testuje **blueprinty** — `SimpleConstant`
i `SimpleObject` třídy, které jsi napsal. Ověřuje dědičnost, tvorbu
instance, změny hodnot, obousměrnou reaktivitu, mutabilitu i vnitřní
lifecycle metody (`_validate`, `_logic`, `_decompose`) — jedním jednotným
vstupním bodem.

```
assert_simple_object                    (hlavní orchestrátor, 3 fáze)
├── SHALLOW
│   ├── assert_class_inheritance
│   └── assert_user_instance_creation
├── PARAMETER (opt-in)
│   ├── assert_value_change
│   ├── assert_reactivity_upward
│   ├── assert_reactivity_downward
│   ├── assert_mutable_behavior
│   └── assert_immutable_behavior
└── DEEP (deep_check=True)
    ├── assert_instance_creation        (s TestMixin)
    ├── assert_validate_method
    ├── assert_calculate_value_method
    └── assert_decompose_value_method
```

---

## 🧭 Obsah

* [`assert_simple_object` — hlavní orchestrátor](#assert_simple_object--hlavní-orchestrátor)
* [Shallow: `assert_class_inheritance`](#shallow-assert_class_inheritance)
* [Shallow: `assert_user_instance_creation`](#shallow-assert_user_instance_creation)
* [Parameter: `assert_value_change` — univerzální jádro](#parameter-assert_value_change--univerzální-jádro)
* [Parameter: `assert_reactivity_upward`](#parameter-assert_reactivity_upward)
* [Parameter: `assert_reactivity_downward`](#parameter-assert_reactivity_downward)
* [Parameter: `assert_mutable_behavior` a `assert_immutable_behavior`](#parameter-assert_mutable_behavior-a-assert_immutable_behavior)
* [Deep: `assert_instance_creation` — synteticky s `TestMixin`](#deep-assert_instance_creation--synteticky-s-testmixin)
* [Deep: `assert_validate_method`](#deep-assert_validate_method)
* [Deep: `assert_calculate_value_method` a `assert_decompose_value_method`](#deep-assert_calculate_value_method-a-assert_decompose_value_method)

---

## `assert_simple_object` — hlavní orchestrátor

**Parametry:**
* `subtests`, `test_class` (povinné).
* `mixins` (výchozí `UNSET`): mixiny pro uživatelskou instanci.
* `test_value_change`, `test_reactivity_up`, `test_reactivity_down`,
  `test_mutability`, `test_immutability` (všechny výchozí `UNSET`) — opt-in
  parametrové testy.
* `verbose` (výchozí `True`), `intro` (výchozí `""`).
* `deep_check` (výchozí `True`): zapíná třetí, "hlubokou" fázi.

**Návratová hodnota:** vytvořená uživatelská instance (s případnými mixiny).

**Tři fáze, stejný vzor jako u `assert_simple_mixin`** (viz
[README_MIXIN_TESTING.md](README_MIXIN_TESTING.md#assert_simple_mixin--hlavní-orchestrátor)) —
shallow → parameter (opt-in) → tady navíc **deep**, třetí fáze:

```python
# SHALLOW
assert_class_inheritance(subtests, test_class, ...)
instance = assert_user_instance_creation(subtests, test_class, mixins=mixins, ...)

# PARAMETER (jen když parametr není UNSET)
if test_value_change is not UNSET: assert_value_change(...)
if test_reactivity_up is not UNSET: assert_reactivity_upward(...)
if test_reactivity_down is not UNSET: assert_reactivity_downward(...)
if test_mutability is not UNSET: assert_mutable_behavior(...)
if test_immutability is not UNSET: assert_immutable_behavior(...)

# DEEP (jen když deep_check=True)
if deep_check:
    assert_instance_creation(subtests, test_class, ...)
    if "_validate" in test_class.__dict__: assert_validate_method(...)
    if "_logic" in test_class.__dict__: assert_calculate_value_method(...)
    if "_decompose" in test_class.__dict__ and test_class.meta.is_decomposeable:
        assert_decompose_value_method(...)
```

**Deep fáze testuje jen to, co uživatel skutečně přepsal.** Všimni si
podmínek `"_validate" in test_class.__dict__` — přesně stejný vzor
lokální přítomnosti, jaký zná `verify_classmethod` (viz
[README_METHOD_PROCESSING.md](README_METHOD_PROCESSING.md#verify_classmethod--brána-validovat-klonovat-nebo-zdědit)).
Nemá smysl jednotkově testovat `_decompose`, pokud ho třída vůbec
nedefinuje (zděděná defaultní implementace vrací `UNSET` a testovat ji by
bylo zbytečné) — a `test_class.meta.is_decomposeable` navíc chrání i před
případem, kdy `_decompose` je definovaná, ale samotná kompozice přesto
není plně dekomponovatelná (protože některý vnitřní prvek dekomponovatelný
není, viz
[README_SIMPLE_OBJECT_METADATA.md](README_SIMPLE_OBJECT_METADATA.md#zpracování-_decompose-a-dekomponovatelnost)).

**Kaskáda `verbose_value_change`** — jemný, ale promyšlený detail:

```python
verbose_value_change = test_value_change is UNSET
# ... po assert_reactivity_upward:
verbose_value_change = verbose_value_change or test_reactivity_up is UNSET
# ... po assert_reactivity_downward:
verbose_value_change = verbose_value_change or test_reactivity_down is UNSET
```

Několik parametrových testů (`assert_reactivity_upward`,
`assert_reactivity_downward`, `assert_mutable_behavior`) interně volá
sdílenou `assert_value_change` (viz níže). Pokud uživatel **už** explicitně
požádal o samostatný test `test_value_change`, nemá smysl, aby stejné
dílčí subtesty reportoval **znovu**, jen zahalené uvnitř jiné, vyšší
kontroly — vedlo by to ke zdvojenému, matoucímu výstupu. Kaskáda
postupně "zapíná" verbose reportování `assert_value_change` jen tehdy,
pokud **žádný** z předchozích testů, které by ji stejně použily, nebyl
požadovaný — jakmile jeden z nich byl (`is UNSET` je `False`), zůstává
`verbose_value_change` vypnuté i pro všechny další.

[▲ Nahoru](#-obsah)

---

## Shallow: `assert_class_inheritance`

**Parametry:** `subtests`, `test_class`, `verbose`, `intro`.

**Návratová hodnota:** `None`.

```python
if not hasattr(test_class, "_inners"):
    assert issubclass(test_class, SimpleConstant)
else:
    assert issubclass(test_class, SimpleObject)
```

Stejné směrovací pravidlo jako `SimpleMeta.__new__` (viz
[README_SIMPLE_META.md](README_SIMPLE_META.md#__new__--vznik-třídy)) —
přítomnost `_inners` rozhoduje, jestli se má třída chovat jako atom, nebo
kompozice, a tenhle assert jen ověřuje, že skutečná dědičnost tomuhle
očekávání odpovídá.

[▲ Nahoru](#-obsah)

---

## Shallow: `assert_user_instance_creation`

**Parametry:** `subtests`, `test_class`, `mixins` (výchozí `UNSET`),
`verbose`, `intro`.

**Návratová hodnota:** vytvořená instance.

```python
mixins_tuple = () if mixins is UNSET else mixins  # (s validací typu)
instance = test_class(mixins=mixins_tuple)
assert instance is not None
```

**Odlišuje se od `assert_instance_creation`** (deep fáze, viz níže) tím,
že je to **lehká, uživatelsky orientovaná** kontrola — ověřuje jen, že se
instance s uživatelem zadanou (nebo žádnou) kombinací mixinů vůbec podaří
vytvořit, bez hlubší strukturální kontroly propagace mixin členů. Vrácená
instance je pak ta, se kterou celý zbytek `assert_simple_object` pracuje
ve fázi PARAMETER.

[▲ Nahoru](#-obsah)

---

## Parameter: `assert_value_change` — univerzální jádro

**Parametry:** `subtests`, `instance`, `value` (raw hodnota, nebo
`InnerValue`), `verbose`, `intro`.

**Návratová hodnota:** aplikovaná hodnota (pro řetězení dál).

**Pět kroků, s guard clause po každém rizikovém:**

```
1. Rozliš cíl — root instance, nebo InnerValue.as_instance_tuple(instance)
   guard: pokud se cesta nedá vyřešit → return None

2. Validuj kandidátní hodnotu (target.validate(value, return_bool=True))
   guard: pokud neplatná → return None (nepokoušet se o setter s neplatnou hodnotou)

3. Ověř, že se hodnota liší od aktuální (jinak by test nic neprokázal)
   guard: pokud stejná → return None

4. Zapiš (target.value = candidate_value), obal v try/except

5. Ověř, že se hodnota skutečně změnila (target.value == candidate_value)
```

**Tohle je nejdůležitější sdílená funkce v celé testovací sadě pro
objekty** — `assert_reactivity_upward`, `assert_reactivity_downward` i
`assert_mutable_behavior` na ni všechny deleguj skutečnou mutaci. Tři
guard clauses **před** kroky 4–5 nejsou samoúčelné: bez nich by test mohl
tiše "projít", i když ve skutečnosti netestoval nic smysluplného (např.
zapsal stejnou hodnotu, jakou instance už měla, takže krok 5 by prošel
triviálně, bez ohledu na to, jestli setter vůbec funguje).

**`InnerValue` jako polymorfní vstup** — parametr `value` přijímá buď
přímo hodnotu (test se aplikuje na `instance` samotnou), nebo `InnerValue`
(test se aplikuje na vnořený prvek, viz
[README_BULK_TEST.md](README_BULK_TEST.md#innervalue--adresa-uvnitř-stromu)).
Tahle jednotná signatura je to, co umožňuje, aby `assert_reactivity_upward`
mohla použít **stejnou** funkci, jakou používá jednoduchý test hodnoty na
kořeni — mění se jen to, **kam** se hodnota zapisuje, ne mechanismus
zápisu samotný.

[▲ Nahoru](#-obsah)

---

## Parameter: `assert_reactivity_upward`

**Parametry:** `subtests`, `instance`, `new_value` (musí být `InnerValue`),
`verbose`, `verbose_value_change`, `intro`.

**Návratová hodnota:** `None`.

```
1. Zapamatuj si původní hodnotu kořene (instance.value)
2. new_value MUSÍ být InnerValue (jinak fail — přímá hodnota nedává smysl
   pro test "reaktivity zdola nahoru", protože není co bublat)
3. assert_value_change(instance, value=new_value)  ── aplikuje se na VNITŘNÍ prvek
4. Ověř, že se kořenová hodnota ZMĚNILA oproti kroku 1
```

**Test je záměrně jednoduchý a nezávislý na konkrétní `_logic`.**
Nekontroluje, jestli je nová hodnota kořene "správná" v nějakém přesném
smyslu — jen že se **vůbec** změnila. To je dostatečné pro ověření, že
mechanismus bublání (`_root_value_setter` → `_recalculate_self`, viz
[README_COMPOSITE_CLASS.md](README_COMPOSITE_CLASS.md#create_recalculate_self--tok-hodnot-nahoru))
skutečně funguje, bez nutnosti duplikovat uživatelovu `_logic` uvnitř
testu.

[▲ Nahoru](#-obsah)

---

## Parameter: `assert_reactivity_downward`

**Parametry:** `subtests`, `instance`, `new_value` (raw hodnota pro
kořen), `verbose`, `verbose_value_change`, `intro`.

**Návratová hodnota:** `None`.

```
1. instance MUSÍ být kompozice (not meta.is_constant)
   guard: atom → fail (nemá vnitřní prvky k testování)

2. meta MUSÍ podporovat dekompozici (is_decomposeable)
   guard: ne → fail

3. assert_value_change(instance, value=new_value)  ── zápis na KOŘEN
4. expected_values = instance.decompose_value(new_value)
   guard: pokud dekompozice spadne → return

5. Pro každý inner: getattr(instance, inner.meta.name_snake) musí sedět
   s odpovídající hodnotou z expected_values (zip podle pořadí)
```

**Test je narozdíl od `assert_reactivity_upward` přesný, ne jen
"změnilo se to".** Protože dekompozice je deterministická funkce
(`decompose_value`), test může spočítat **přesně**, jakou hodnotu by měl
mít každý vnitřní prvek, a porovnat to 1:1. To je možné právě proto, že
`_recalculate_inners` (viz
[README_COMPOSITE_CLASS.md](README_COMPOSITE_CLASS.md#create_recalculate_inners--tok-hodnot-dolů))
používá tu samou `decompose_value` metodu, kterou test volá pro výpočet
očekávané hodnoty — test tedy v podstatě ověřuje, že runtime chování
odpovídá tomu, co by "ručně" spočítal někdo zvenčí.

[▲ Nahoru](#-obsah)

---

## Parameter: `assert_mutable_behavior` a `assert_immutable_behavior`

Dva symetrické testy, každý pro jednu polovinu mutability kontraktu.

### `assert_mutable_behavior`

**Parametry:** `subtests`, `test_class`, `new_value`, `verbose`,
`verbose_value_change`, `intro`.

```
1. instance = test_class(mutable=True)
2. original_id = id(instance)
3. assert_value_change(instance, value=new_value)   ← skutečná mutace
4. id(instance) MUSÍ zůstat stejné jako original_id
```

### `assert_immutable_behavior`

**Parametry:** `subtests`, `test_class`, `new_value`, `verbose`, `intro`.

```
1. instance = test_class(mutable=False)
2. original_id, original_value = id(instance), instance.value
3. instance.value = new_value  MUSÍ vyhodit výjimku
4. id(instance) MUSÍ zůstat stejné
5. instance.value MUSÍ zůstat stejné jako original_value
```

**Oba testy sdílí stejnou kontrolu identity** (`id(instance)` beze
změny), ale s **opačným** očekáváním u samotné mutace: mutable **musí**
uspět a zachovat identitu, immutable **musí** selhat a zachovat identitu
i hodnotu. Tahle symetrie přesně odpovídá tomu, jak je immutabilita
implementovaná na úrovni `create_value_property`/`create_value_setter` —
u immutable varianty setter **neexistuje** (viz
[README_VALUE_PROPERTIES.md](README_VALUE_PROPERTIES.md#create_value_property--sestavení-property)),
takže pokus o zápis nikdy neuspěje na úrovni samotného Pythonu, ne až na
nějaké byznys validaci.

**Kontrola identity je klíčová pro obě varianty** — potvrzuje, že systém
implementuje **skutečnou** mutabilitu (in-place změna stavu), ne vzor
"immutable-style" objektů, kde by každá "změna" ve skutečnosti vytvářela
novou instanci. `assert_mutable_behavior` dokazuje, že mutace nevytváří
novou instanci; `assert_immutable_behavior` dokazuje, že odmítnutá mutace
nezanechá žádnou vedlejší stopu.

[▲ Nahoru](#-obsah)

---

## Deep: `assert_instance_creation` — synteticky s `TestMixin`

**Parametry:** `subtests`, `test_class`, `verbose`, `intro`.

**Návratová hodnota:** vytvořená instance s `TestMixin`.

```python
instance = test_class(mixins=(TestMixin,))

assert instance._test_slot == "test_value"                              # slot
assert instance.test_property == "test_value"                           # property
assert instance.test_method() == "[TestMixin] property=test_value"      # metoda
assert instance.__class__.test_class_attribute == "class_level_ok"      # class atribut
assert instance.test_class_method() == "class_method_ok"                # class metoda
```

**Na rozdíl od `assert_user_instance_creation` tenhle test nepoužívá
uživatelovy mixiny — vždy `TestMixin`.** Účel je jiný: neověřuje, jestli
funguje **konkrétní** uživatelský mixin (to dělá
[`assert_simple_mixin`](README_MIXIN_TESTING.md)), ale jestli **mechanismus
připojování mixinů obecně** funguje pro daný `test_class` — tedy jestli
`_resolve_flat_mixins`/`_build_instance_class_dict`/`_extend_instance_class`
(viz [README_CREATE_INSTANCE.md](README_CREATE_INSTANCE.md)) fungují
korektně přesně na téhle konkrétní blueprint třídě. `TestMixin` (viz
[README_BULK_TEST.md](README_BULK_TEST.md#testmixin--syntetický-testovací-dvojník))
je navržený tak, aby pokrýval **všechny** cesty injekce najednou — slot,
property, instanční metodu, class atribut i class metodu (přes
`__extend_instance_class__`) — jedním voláním.

[▲ Nahoru](#-obsah)

---

## Deep: `assert_validate_method`

**Parametry:** `subtests`, `test_class`, `verbose`, `intro`.

**Návratová hodnota:** `None`.

**Pět kontrol, systematicky pokrývající "šťastnou cestu" i dva neplatné vstupy × dva režimy:**

```
1. test_class.validate(meta.default, return_bool=True)  MUSÍ být True
2. test_class.validate(UNSET, return_bool=True)          MUSÍ být False
3. test_class.validate(UNSET, return_bool=False)          MUSÍ vyhodit výjimku
4. test_class.validate(None, return_bool=True)            MUSÍ být False
5. test_class.validate(None, return_bool=False)           MUSÍ vyhodit výjimku
```

**Matice 2×2 (`UNSET`/`None` × boolean/exception mód) systematicky
ověřuje obě poloviny kontraktu `validate`** popsaného v
[README_SIMPLE_CONSTANT.md](README_SIMPLE_CONSTANT.md#validate) — že
`return_bool=True` vždy vrací bool bez výjimky, a `return_bool=False`
vždy buď vrátí (implicitně) úspěch, nebo vyhodí strukturovanou chybu,
nikdy ne obojí zaměněné. `UNSET` a `None` jsou vybrané jako dva
"univerzálně neplatné" vstupy, protože žádný smysluplný `_type` by je
neměl akceptovat — jsou to tedy spolehlivé negativní testovací případy
nezávislé na konkrétní doméně testované třídy.

[▲ Nahoru](#-obsah)

---

## Deep: `assert_calculate_value_method` a `assert_decompose_value_method`

Dva symetrické testy pro kompozice — jeden pro směr nahoru (výpočet),
druhý pro směr dolů (rozklad).

### `assert_calculate_value_method`

```python
params = {inner.meta.name_snake: inner.meta.default for inner in test_class.meta.inners}
calculated = test_class.calculate_value(**params)
assert calculated == test_class.meta.default
```

### `assert_decompose_value_method`

```python
expected = tuple(inner.meta.default for inner in test_class.meta.inners)
decomposed = test_class.decompose_value(test_class.meta.default)
assert decomposed == expected
```

**Oba testy fungují na stejném principu — testují proti defaultům,
protože defaulty jsou jediné hodnoty, o kterých už systém s jistotou ví,
že jsou platné a vzájemně konzistentní.** Vzpomeň si, že `self.default`
kompozice **je** výsledek dry-runu `_logic` nad defaulty `_inners` (viz
[README_SIMPLE_OBJECT_METADATA.md](README_SIMPLE_OBJECT_METADATA.md#zpracování-_logic-a-odvození-defaultu)) —
`assert_calculate_value_method` tedy v podstatě **zopakuje** ten samý
výpočet, který už jednou proběhl při definici třídy, a ověří, že dává
stejný výsledek (deterministicky, žádný postranní efekt mezi tím
neproběhl).

**`assert_decompose_value_method` navíc ověřuje obousměrnou konzistenci**
mezi `_logic` a `_decompose` — pokud `_logic(defaulty) == default` a
`_decompose(default) == defaulty`, znamená to, že jsou tyhle dvě funkce
skutečně vzájemné inverze, aspoň na téhle jedné (defaultní) hodnotě. To
je přesně vlastnost, kterou `verify_decompose_outcome` (viz
[README_METHOD_PROCESSING.md](README_METHOD_PROCESSING.md#verify_decompose_outcome--speciální-pravidla-pro-_decompose))
kontroluje strukturálně už při definici třídy — tenhle test to jen
znovu potvrzuje na úrovni chování, ne jen typové shody.

[▲ Nahoru](#-obsah)

➡️ Pokračování: [README_BULK_TEST.md](README_BULK_TEST.md)
