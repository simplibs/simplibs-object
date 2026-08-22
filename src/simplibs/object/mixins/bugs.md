# Kontrolní seznam podezřelých bugů — před spuštěním testů mixinů

Toto je scénář pro ranní kontrolu, **než** spustíš testovací sadu. U každého bodu:
soubor → co se děje → co zkontrolovat → návrh opravy → který test to prověří.

Řazeno podle toho, jak na sebe věci navazují (od nejhlubší infrastruktury nahoru),
ne podle závažnosti.

---

## 1. `reacalculate_owner_value` — rozbalení dict klíčů místo hodnot

**Soubor:** `mixins/_common_logic/immutability/with_constant/utils/reacalculate_owner_value.py`

**O co jde:**
Funkce přepočítává hodnotu vlastníka (owner) na základě aktuálních hodnot jeho inners.
Volání vypadá přibližně takto:

```python
new_value = owner.logic(*owner_inners_value_dict)
```

Hvězdička před `dict` rozbalí jeho **klíče** (řetězce se jmény), ne hodnoty. Pokud je to
skutečně takto v kódu, `owner.logic("first", "second")` dostane jména namísto čísel.

**Co zkontrolovat:**
Otevři soubor a podívej se, jak přesně je `owner.logic(...)` volané. Hledej řádek
s hvězdičkou před proměnnou typu dict.

**Návrh opravy (pokud bug potvrzen):**
```python
# místo:
new_value = owner.logic(*owner_inners_value_dict)

# buď podle jmen (kwargs):
new_value = owner.logic(**owner_inners_value_dict)

# nebo pozičně podle hodnot:
new_value = owner.logic(*owner_inners_value_dict.values())
```
Zvol variantu podle toho, jestli `logic()` očekává pozicní nebo pojmenované argumenty
(u `_logic` classmethod v `SimpleObjectMetadata` jsou parametry pojmenované podle
`inners_params_name`, takže `**kwargs` je pravděpodobně správně).

**Test, který to prověří:**
`tests/mixins/_commons/immutability/with_constant/utils/test_reacalculate_owner_value.py`
(a nepřímo i `test_with_constant.py`, `test_with_composite.py` atd. — pokud je tohle
rozbité, spadne toho víc najednou).

---

## 2. `to_dict` — IndexError na čistém atomu

**Soubor:** `mixins/core_mixins/_utils/serialization/to_dict.py`

**O co jde:**
Pro čistý atom (instance bez `_inners`) je jeho vlastní uzel v `_nodes_tuple` uložen
s `path == ()` (prázdný tuple). Kód dělá:

```python
last_key = path[0]
```

Na prázdném tuple `path[0]` vyhodí `IndexError`. Serializace čistého atomu (`to_dict()`
na instanci, co má `mixins=(Serialization,)` a je vytvořená přes `as_atom=True` bez
jakýchkoliv inners) by tedy měla spadnout.

**Co zkontrolovat:**
Zkus ručně (v konzoli/skriptu) tohle:
```python
class Foo(SimpleConstant):
    _type = int
    _default = 1

instance = Foo(mixins=(Serialization,), as_atom=True)
instance.to_dict()
```
Pokud to spadne na `IndexError: tuple index out of range`, bug je potvrzený.

**Návrh opravy:**
```python
last_key = path[0] if path else instance.meta.name_snake
```
nebo elegantněji ošetřit prázdnou cestu jako speciální případ na začátku smyčky.

**Test, který to prověří:**
`tests/mixins/core_mixins/_utils/serialization/test_to_dict.py` →
`TestToDict::test_atom_serialization`

---

## 3. `from_dict` — stejný IndexError problém, jiná strana

**Soubor:** `mixins/core_mixins/_utils/serialization/from_dict.py`

**O co jde:**
Analogický problém jako bod 2, ale kód tu používá:
```python
last_key = path[-1]
```
Stejně tak `path[-1]` na prázdném tuple vyhodí `IndexError`.

**Co zkontrolovat:**
```python
instance = Foo(mixins=(Serialization,), as_atom=True, mutable=True)
instance.from_dict({"foo": 5, "_owner_class": instance.meta.owner_class})
```
(uprav klíč podle skutečného `name_snake`). Pokud spadne na `IndexError`, potvrzeno.

**Návrh opravy:**
Stejný princip jako u bodu 2 — ošetřit prázdnou `path` jako speciální případ, typicky
`last_key = path[-1] if path else instance.meta.name_snake`.

**Poznámka:** Pokud opravíš bod 2 a bod 3 stejným způsobem, zvaž vytažení té podmínky
do sdílené pomocné funkce (mají koneckonců úplně stejný tvar problému).

**Test, který to prověří:**
`tests/mixins/core_mixins/_utils/serialization/test_from_dict.py` →
`TestFromDictImmutable`/`TestFromDictMutable` (testy na atomech nejsou explicitně
napsané — pokud opravíš bug, klidně mrkni, jestli chceš, abych doplnil i explicitní
atom test analogicky k `to_dict`).

---

## 4. `process_single_change` — NameError místo validační chyby

**Soubor:** `mixins/_common_logic/immutability/with_any/utils/process_single_change.py`

**O co jde:**
Validační větev v kódu odkazuje na proměnnou `inner_tuple`, ale parametr funkce se
jmenuje `change`. Při neplatném vstupu (např. `change` není 2-tuple) by tedy měl
nastat `NameError: name 'inner_tuple' is not defined` místo srozumitelné strukturované
chyby.

**Co zkontrolovat:**
Otevři soubor a najdi řádek s `inner_tuple` — ověř, že je to skutečně překlep a né
záměrně jinak pojmenovaná proměnná odjinud.

**Návrh opravy:**
Přejmenovat `inner_tuple` → `change` (nebo naopak přejmenovat parametr funkce, podle
toho, co dává větší smysl v kontextu zbytku souboru).

**Test, který to prověří:**
`tests/mixins/_commons/immutability/with_any/utils/test_process_single_change.py` —
pozor, testy tam projdou i s bugem (protože `NameError` je taky `Exception`), takže
tenhle bug testy same o sobě NEODHALÍ jako selhání. Doporučuju po opravě ručně
zkontrolovat, že chybová hláška je teď smysluplná (např. přidat `pytest.raises(SomeSpecificError, match=...)` misto obecného `Exception`).

---

## 5. `process_up_limit_value` / `process_down_limit_value` — porovnání s UNSET

**Soubor:**
`mixins/others/numerical/_stepper_class/processors/process_up_limit_value.py`
`mixins/others/numerical/_stepper_class/processors/process_down_limit_value.py`

**O co jde:**
Výchozí `up_limit`/`down_limit` na `Stepper` je `UNSET`. Kód dělá:
```python
# v process_up_limit_value:
if self.down_limit > _value: ...

# v process_down_limit_value:
if self.up_limit < _value: ...
```
Otázka je, jestli `UnsetType` (z `simplibs.sentinels`) podporuje porovnávací operátory
(`<`, `>`) s čísly. Pokud ano a vrací např. vždy `False`, všechno je v pořádku. Pokud
ne, nastavení JEN JEDNOHO limitu (bez toho druhého) spadne na `TypeError`.

**Co zkontrolovat:**
```python
from simplibs.sentinels import UNSET
UNSET > 5   # spadne, nebo vrátí False/True?
UNSET < 5
```
Zkus tohle přímo v konzoli. Pokud to spadne na `TypeError`, bug je potvrzený a je
docela zásadní — znamená to, že nastavit `up_limit` bez předchozího `down_limit` (nebo
naopak) je aktuálně nemožné, což je dost omezující UX pro `Stepper`/`Volume`/`Equalizer`.

**Návrh opravy (pokud bug potvrzen):**
```python
# v process_up_limit_value:
if self.down_limit is not UNSET and self.down_limit > _value: ...

# v process_down_limit_value:
if self.up_limit is not UNSET and self.up_limit < _value: ...
```

**Test, který to prověří:**
`tests/mixins/others/numerical/_stepper_class/processors/test_process_up_limit_value.py`
→ `test_set_up_limit_without_down_limit_first`
`tests/mixins/others/numerical/_stepper_class/processors/test_process_down_limit_value.py`
→ `test_set_down_limit_without_up_limit_first`

---

## 6. `assert_simple_mixin` — chybí parametr `mutable`

**Soubor:** `testing/assert_simple_mixin.py` a `testing/asserts/mixins/assert_mixin_instance_creation.py`

**O co jde:** Tohle NENÍ bug v mixinech samotných, ale limitace v testovací utilitě.
`assert_mixin_instance_creation` volá `test_class(mixins=(mixin_class,))` bez
možnosti předat `mutable`. Výchozí hodnota je `mutable=True`. Pro mixiny s
`_immutable_only=True` (`ImmutableMethods`, `ImmutableWithInners`) to vždy selže na
validaci kompatibility.

**Co zkontrolovat:** Nic — to je jen k vědomí. V testech jsem to obešel ručním
vytvořením instance s `mutable=False` místo použití `assert_simple_mixin` u těchto
dvou mixinů (viz `tests/mixins/others/immutable/`).

**Návrh (volitelné vylepšení, ne oprava bugu):**
Pokud chceš `assert_simple_mixin` použít i pro budoucí `_immutable_only` mixiny bez
obcházení, zvaž přidání volitelného `mutable: bool = True` parametru, který se
propaguje až do `test_class(mixins=(mixin_class,), mutable=mutable)`.

**Test, který to prověří:** Netýká se konkrétního testu — je to poznámka k
`tests/mixins/others/immutable/test_ImmutableMethods.py` a
`test_ImmutableMethodsWithInners.py`, proč tam vypadá struktura jinak než jinde.

---

## Doporučený postup na zítra

1. Projdi body 1–5 v tomto pořadí (odspoda nahoru podle závislostí — `with_constant`
   je základ, na kterém stojí `with_composite`/`with_any`/`Serialization`).
2. U každého bodu nejdřív rychle ověř v konzoli/skriptu, jestli bug skutečně nastává
   (kód výše ti to usnadní).
3. Pokud potvrzeno → oprav → spusť příslušný test soubor izolovaně
   (`pytest tests/cesta/k/souboru.py -v`), ať vidíš hned, jestli oprava sedí.
4. Bod 6 si jen přečti, žádná akce nutná (leda že bys chtěl `assert_simple_mixin`
   rozšířit).
5. Až budou body 1–5 vyřešené, spusť celou sadu (`pytest tests/mixins/ -v`) a projdi
   zbytek red testů — mohou se objevit další drobnosti, které jsme cestou nemohli
   předvídat bez spuštěného kódu.

Hodně štěstí! 🙂