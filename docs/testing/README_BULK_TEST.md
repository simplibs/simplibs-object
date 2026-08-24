# 📦 Hromadné testování — `bulk_test` a kontejnery

`bulk_test` je poslední vrstva testovací sady — umožňuje spustit **celou
dávku** testů (objekty i mixiny, v libovolné kombinaci) jedním voláním
uvnitř jediné pytest testovací funkce, místo psaní desítek samostatných
`def test_...` funkcí. Podporuje dva styly zápisu: rychlý (holé třídy a
tuply) a deklarativní (`ObjectCase`/`MixinCase` kontejnery).

```
bulk_test                          (polymorfní dispečer)
├── ObjectCase.run_test()  ──► assert_simple_object(README_OBJECT_TESTING.md)
├── MixinCase.run_test()   ──► assert_simple_mixin(README_MIXIN_TESTING.md)
├── holá SimpleConstant/SimpleObject třída  ──► assert_simple_object (bez mixinů)
├── (třída, mixiny)  ──► assert_simple_object (s mixiny)
└── (mixin, třída)   ──► assert_simple_mixin
```

---

## 🧭 Obsah

* [`bulk_test` — polymorfní dispečer](#bulk_test--polymorfní-dispečer)
* [`TestMixin` — syntetický testovací dvojník](#testmixin--syntetický-testovací-dvojník)
* [`InnerValue` — adresa uvnitř stromu](#innervalue--adresa-uvnitř-stromu)
* [`ObjectCase` a `MixinCase` — deklarativní specifikace](#objectcase-a-mixincase--deklarativní-specifikace)

---

## `bulk_test` — polymorfní dispečer

**Parametry:** `subtests`, `items` (list/tuple libovolně smíchaných
položek), `verbose` (výchozí `True`), `deep_check` (výchozí `True`).

**Návratová hodnota:** `None` (spouští asserty přímo).

**Pět rozpoznávaných tvarů položek, testovaných v tomhle pořadí:**

```python
for item in items:
    if isinstance(item, ObjectCase):
        item.run_test(subtests, ...)
        continue

    if isinstance(item, MixinCase):
        item.run_test(subtests, ...)
        continue

    if isinstance(item, type) and issubclass(item, SimpleConstant):
        assert_simple_object(subtests, item, mixins=UNSET, ...)
        continue

    if isinstance(item, tuple) and len(item) == 2:
        # (SimpleConstant třída, tuple mixinů) → assert_simple_object s mixiny
        # (mixin, SimpleConstant třída) → assert_simple_mixin
        ...
        continue

    raise AssertionError(f"Unsupported bulk test item: {item!r}")
```

**Rozlišení dvou variant dvouprvkového tuple je typová detekce, ne
poziční konvence.** `(cls, mixins)` vs. `(mixin_class, test_class)` — obojí
je syntakticky `tuple` o délce 2, takže dispečer musí prozkoumat **typy**
obou prvků, aby poznal, o kterou variantu jde:

```python
cls, mixins = item
if (isinstance(cls, type) and issubclass(cls, SimpleConstant)
    and isinstance(mixins, tuple) and all(issubclass(m, SimpleMixin) for m in mixins)):
    # → objekt + mixiny

mixin_class, test_class = item
if (isinstance(mixin_class, type) and issubclass(mixin_class, SimpleMixin)
    and isinstance(test_class, type) and issubclass(test_class, SimpleConstant)):
    # → mixin + testovací třída
```

Obě podmínky se zkouší v pořadí (nejdřív "objekt + mixiny", pak "mixin +
třída") — a protože se navzájem typově vylučují (`SimpleConstant`
podtřída nemůže být zároveň `SimpleMixin` podtřída), nemůže dojít ke
kolizi. Cokoliv, co neodpovídá ani jednomu z pěti rozpoznaných tvarů,
skončí na explicitním `raise AssertionError` — **fail-fast** princip:
lepší okamžitě nahlásit neplatnou položku dávky, než ji tiše přeskočit a
nechat uživatele myslet si, že test proběhl.

**`intro` se generuje automaticky z jména třídy** (`f"object_{cls.__name__}::"`,
`f"mixin_{mixin_class.__name__}::"`) — díky tomu i hromadně spuštěná dávka
desítek položek produkuje **čitelné, navzájem odlišitelné** názvy subtestů
v pytest výstupu, bez nutnosti, aby to uživatel u každé položky ručně
vypisoval.

[▲ Nahoru](#-obsah)

---

## `TestMixin` — syntetický testovací dvojník

Speciální mixin, který **neexistuje pro produkční použití** — jeho jediný
účel je sloužit jako "univerzální rentgen" pro ověření, že mechanismus
injekce mixinů (viz
[README_CREATE_INSTANCE.md](README_CREATE_INSTANCE.md)) funguje správně
na libovolné cílové třídě.

```python
class TestMixin(SimpleMixin):
    __test__ = False  # pytest ho nemá brát jako testovací třídu

    _constant_only = False
    _composite_only = False
    _mutable_only = False
    _immutable_only = False
    _only_types = UNSET

    __slots__ = ("_test_slot",)

    def init_mixins(self) -> None:
        self._test_slot = "test_value"

    @property
    def test_property(self) -> str: ...

    def test_method(self) -> str: ...

    @staticmethod
    def __extend_instance_class__(instance_cls: type) -> type:
        setattr(instance_cls, "test_class_attribute", "class_level_ok")
        def test_class_method(self) -> str: return "class_method_ok"
        setattr(instance_cls, "test_class_method", test_class_method)
        return instance_cls
```

**Všechny kompatibilní příznaky jsou vypnuté (`False`/`UNSET`)** — tohle
je záměrné a klíčové. `TestMixin` musí jít připojit k **úplně libovolné**
kombinaci atom/kompozice × mutable/immutable, protože jeho úkolem je
testovat mechanismus injekce nezávisle na tom, jaký konkrétní
`test_class` zrovna testuješ (viz
[`_verify_mixin_compatibility`](README_CREATE_INSTANCE.md#_verify_mixin_compatibility--kompatibilní-matice) —
kdyby `TestMixin` měl třeba `_constant_only = True`, spadl by na
kompozicích).

**Pokrývá všech pět cest injekce najednou, jedním mixinem:**

| Mechanismus | Co ověřuje |
|---|---|
| `__slots__ = ("_test_slot",)` | alokace slotu na dynamické třídě |
| `init_mixins` | spuštění inicializačního hooku (viz [`_build_combined_init_mixins`](README_CREATE_INSTANCE.md#_build_combined_init_mixins--řetězení-inicializace)) |
| `test_property` | property (getter i setter) se do namespace zkopírovala správně |
| `test_method` | instanční metoda funguje a vidí stav nastavený v `init_mixins` |
| `__extend_instance_class__` | post-kompilační hook (viz [`_extend_instance_class`](README_CREATE_INSTANCE.md#_extend_instance_class--post-kompilační-hooky)) funguje a umí přidat class-level atributy i metody |

`__test__ = False` je čistě technický detail pro pytest — bez něj by
pytest mohl zkusit "objevit" `TestMixin` jako testovací třídu samotnou
(protože její jméno začíná `Test...`), což by generovalo falešné varování.

[▲ Nahoru](#-obsah)

---

## `InnerValue` — adresa uvnitř stromu

**Dataclass** (`frozen=True`) reprezentující "cestu + hodnotu" pro
testování vnořených prvků kompozice — používá ho
`assert_value_change`/`assert_reactivity_upward` (viz
[README_OBJECT_TESTING.md](README_OBJECT_TESTING.md#parameter-assert_value_change--univerzální-jádro)).

**Pole:** `path` (`str` s tečkovou notací, nebo `Iterable[str]`), `value` (`Any`).

**Normalizace cesty v `__post_init__`:**
```python
if isinstance(self.path, str):
    parts = self.path.split(".")
else:
    parts = tuple(self.path)

if not parts:
    raise_inner_value_empty_path()
for part in parts:
    if not isinstance(part, str):
        raise_inner_value_invalid_path_type(self.path, part)

object.__setattr__(self, "path", tuple(parts))
```

**Dva zápisy cesty, jeden normalizovaný výsledek** — `InnerValue("engine.pistons",
4)` a `InnerValue(("engine", "pistons"), 4)` po `__post_init__` dopadnou
úplně stejně. Tohle je stejný vzor "přijmi pohodlný vstup, normalizuj na
jednotnou vnitřní reprezentaci", jaký znáš z
[`assert_mixins_slots_values`](README_MIXIN_TESTING.md#assert_mixins_slots_values--kontrola-hodnot-slotů) —
jen aplikovaný na cestu ve stromu místo na pár jméno/hodnota.

**`object.__setattr__` na frozen dataclass** — `InnerValue` je `frozen=True`
(neměnná, hashovatelná hodnota), takže normální `self.path = tuple(parts)`
by selhalo na `FrozenInstanceError`. `object.__setattr__(self, "path",
...)` obchází tenhle zámek přesně jednou, uvnitř `__post_init__` — legitimní,
běžný vzor pro frozen dataclassy, kdy potřebuješ dopočítat/normalizovat
pole při inicializaci.

**Navigace stromem — `as_instance_tuple`:**
```python
def as_instance_tuple(self, instance):
    current = instance
    for part in self.path:
        inner_prop = f"{part}_instance"
        if not hasattr(current, inner_prop):
            return UNSET
        current = getattr(current, inner_prop)
        if current is None:
            return UNSET
    return current, self.value
```

**Používá konvenci `<jméno>_instance`**, tedy přesně tu property, kterou
generuje `create_properties_for_inner` (viz
[README_VALUE_PROPERTIES.md](README_VALUE_PROPERTIES.md#create_properties_for_inner--obě-dohromady-pro-jeden-prvek)) —
`InnerValue("engine", 4)` tedy interně sáhne na `instance.engine_instance`,
ne na `instance.engine` (což by vrátilo hodnotu, ne instanci, na které
lze dál pokračovat v navigaci hlouběji do stromu). Vrací se `UNSET` (ne
výjimka) při jakémkoliv selhání navigace — volající (`assert_value_change`)
to pak zpracuje jako `pytest.fail` s kontextem, místo aby se test rozbil
na necitovaném `AttributeError` z hloubky helper funkce.

[▲ Nahoru](#-obsah)

---

## `ObjectCase` a `MixinCase` — deklarativní specifikace

Dvě `dataclass` (`slots=True, kw_only=True`), které dělají přesně jednu
věc: **zabalí parametry** `assert_simple_object`/`assert_simple_mixin` do
pojmenovaného, znovupoužitelného objektu.

```python
@dataclass(slots=True, kw_only=True)
class ObjectCase:
    test_class: "SimpleClassLike"
    mixins: tuple[...] | UnsetType = UNSET
    test_value_change: Any | InnerValue | UnsetType = UNSET
    test_reactivity_up: InnerValue | UnsetType = UNSET
    test_reactivity_down: Any | UnsetType = UNSET
    test_mutability: Any | InnerValue | UnsetType = UNSET
    test_immutability: Any | InnerValue | UnsetType = UNSET

    def run_test(self, subtests, *, verbose=True, intro="", deep_check=True):
        from ..assert_simple_object import assert_simple_object
        return assert_simple_object(subtests, self.test_class, mixins=self.mixins, ...)
```

`MixinCase` je strukturálně identická myšlenka, jen se zrcadlí parametry
`assert_simple_mixin` (`mixin_class`, `test_class`, `slots_names`,
`slots_values`, `attribute_names`, `method_names`).

**Proč tenhle obal vůbec existuje, když `bulk_test` umí i holé tuply?**
Tuply (`(cls, mixins)`, `(mixin, cls)`) pokrývají jen ty **nejběžnější**
parametry — nedávají prostor pro `test_reactivity_up`, `slots_values` a
podobné jemnější nastavení. `ObjectCase`/`MixinCase` naopak vystavují
**celou** paletu parametrů orchestrátorů, a navíc jsou **pojmenované** —
čitelnější než pozičně skládaný tuple, obzvlášť když je testovací sada
velká a testovací případy se v repozitáři sdílí/importují mezi soubory.

**Lokální import uvnitř `run_test`** (`from ..assert_simple_object import
assert_simple_object`) — ne na vrcholu modulu — je vědomé řešení
cyklické závislosti: `assert_simple_object` interně importuje `ObjectCase`
(pro typové anotace), takže import na vrcholu `ObjectCase.py` by vytvořil
kruh. Import uvnitř metody se vyhodnotí až při skutečném volání
`run_test()`, kdy už jsou oba moduly plně načtené.

[▲ Nahoru](#-obsah)

➡️ Pokračování: [README_TESTING_OVERVIEW.md](README_TESTING_OVERVIEW.md)
