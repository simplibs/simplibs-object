Ráda ti v tom udělám jasno. Ten velký třesk v typování přišel s **Pythonem 3.9** (přesněji skrze PEP 585). Od té doby platí jednoduché pravidlo: **Pokud v Pythonu existuje vestavěný typ (built-in) nebo třída v `collections.abc`, používej přednostně ji, a ne její kopii velkým písmenem z modulu `typing`.**

Tady je kompletní přehled těch nejdůležitějších prvků, které jsou označené jako *Deprecated* (zastaralé), a čím se nahrazují.

---

## 1. Základní kolekce (Vestavěné typy)

Tyto typy z `typing` se od verze 3.9 píší jednoduše s **malým písmenem** a importují se přímo z vestavěného jmenného prostoru (nemusíš pro ně nic importovat).

| Starý zápis (`typing`) | Nový zápis (Vestavěný) | Příklad použití |
| --- | --- | --- |
| `typing.List` | `list` | `list[str]` |
| `typing.Dict` | `dict` | `dict[str, int]` |
| `typing.Tuple` | `tuple` | `tuple[int, ...]` |
| `typing.Set` | `set` | `set[int]` |
| `typing.FrozenSet` | `frozenset` | `frozenset[str]` |
| `typing.Type` | `type` | `type[MyClass]` |

---

## 2. Abstraktní kolekce (Přesun do `collections.abc`)

Tyto typy reprezentují rozhraní (např. "jakýkoliv slovník", "jakákoliv sekvence") a nově se importují z modulu `collections.abc`.

| Starý zápis (`typing`) | Nový zápis (`collections.abc`) | Význam |
| --- | --- | --- |
| `typing.Callable` | `Callable` | Cokoliv, co lze zavolat (funkce, třída) |
| `typing.Iterable` | `Iterable` | Cokoliv, přes co lze cyklit (`for` cyklus) |
| `typing.Iterator` | `Iterator` | Samotný iterátor (má metodu `__next__`) |
| `typing.Sequence` | `Sequence` | Prvky s indexem a délkou (read-only `list`, `tuple`, `str`) |
| `typing.Mapping` | `Mapping` | Read-only struktura klíč-hodnota (jako `dict`) |
| `typing.MutableMapping` | `MutableMapping` | Zapisovatelná struktura klíč-hodnota |
| `typing.Set` (jako ABC) | `Set` | Obecná množina |

---

## 3. Regulární výrazy (Přesun do `re`)

Pokud typuješ zkompilovaný regulární výraz nebo nalezené shody, typy se přesunuly přímo do modulu `re`.

| Starý zápis (`typing`) | Nový zápis (`re`) |
| --- | --- |
| `typing.Pattern` nebo `typing.re.Pattern` | `re.Pattern` |
| `typing.Match` nebo `typing.re.Match` | `re.Match` |

---

## 4. Bonus: Co se změnilo v Pythonu 3.10 (`Union` a `Optional`)

Sice nejsou oficiálně označené za *deprecated* ve smyslu, že by se z Pythonu hned odstraňovaly, ale v moderním kódu se už téměř nepoužívají, protože mají mnohem elegantnější náhradu pomocí **roury (`|`)**:

* **`typing.Union[int, str]`** $\rightarrow$ nahrazeno za **`int | str`**
* **`typing.Optional[int]`** (což je ekvivalent k `Union[int, None]`) $\rightarrow$ nahrazeno za **`int | None`**

---

### Shrnutí pro tvůj kód: Co ti v `typing` ZŮSTÁVÁ?

V modulu `typing` dál zůstávají věci, které nemají přímý vestavěný ekvivalent v Pythonu pro běhové prostředí (runtime). Typicky tam budeš stále hledat:

* `Any`
* `TYPE_CHECKING`
* `Protocol` (pro strukturální podtypování, jako jsou tvoje mixiny)
* `Generic` / `TypeVar` (pro generické třídy)
* `Literal` (pro omezení na specifické hodnoty)
* `Self` (od Pythonu 3.11 pro typování metod vracejících `self`)