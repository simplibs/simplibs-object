# 🧪 Testování mixinů — `assert_simple_mixin` a jeho stavební bloky

Tenhle dokument popisuje testovací sadu určenou speciálně pro ověřování
mixinů — jestli správně dědí ze `SimpleMixin`, jestli se dají bez chyby
připojit k blueprintu přes `mixins=(...)`, a jestli po připojení skutečně
poskytují sloty, atributy a metody, které slibují. Je to konkrétní
naplnění principu zmíněného v historii projektu: `assert_simple_mixin` je
hlavní vstupní bod, `assert_simple_object`/`assert_simple_mixin` používají
stejný vzor "orchestrátor + izolované dílčí asserty".

```
assert_simple_mixin                    (hlavní orchestrátor)
├── assert_mixin_inheritance            (dědí mixin ze SimpleMixin?)
├── assert_mixin_instance_creation      (dá se připojit a vytvořit instance?)
├── assert_instance_hasattr             (existují očekávané sloty/atributy/metody?)
└── assert_mixins_slots_values          (mají sloty očekávané hodnoty?)
```

---

## 🧭 Obsah

* [`assert_simple_mixin` — hlavní orchestrátor](#assert_simple_mixin--hlavní-orchestrátor)
* [`assert_mixin_inheritance` — kontrola dědičnosti](#assert_mixin_inheritance--kontrola-dědičnosti)
* [`assert_mixin_instance_creation` — vytvoření a injekce](#assert_mixin_instance_creation--vytvoření-a-injekce)
* [`assert_instance_hasattr` — obecná brána přítomnosti](#assert_instance_hasattr--obecná-brána-přítomnosti)
* [`assert_mixins_slots_values` — kontrola hodnot slotů](#assert_mixins_slots_values--kontrola-hodnot-slotů)
* [Jak to všechno zapadá dohromady](#jak-to-všechno-zapadá-dohromady)

---

## `assert_simple_mixin` — hlavní orchestrátor

**Parametry:**
* `subtests` (*Any*): nativní pytest `subtests` fixture.
* `mixin_class` (*SimpleMixinType*): testovaný mixin.
* `test_class` (*SimpleClassType*): blueprint třída, na kterou se mixin připojí.
* `mutable` (*bool*, výchozí `True`).
* `slots_names`, `slots_values`, `attribute_names`, `method_names`
  (volitelné, výchozí `UNSET`): co všechno se má na výsledné instanci ověřit.
* `verbose` (*bool*, výchozí `True`).
* `intro` (*str*, výchozí `""`): prefix pro jména subtestů.

**Návratová hodnota:** vytvořená instance s připojeným mixinem (pro
případné další, uživatelsky specifické testy), nebo `None`, pokud selhala
už samotná tvorba instance.

**Dvě fáze, v tomhle pořadí:**

```
1. SHALLOW TESTS (základní smlouva)
   ├─ assert_mixin_inheritance
   └─ assert_mixin_instance_creation  ──► vrací instanci (nebo None)

   guard: pokud instance is None → return None, dál se nepokračuje

2. PARAMETER TESTS (volitelné, jen pokud parametr není UNSET)
   ├─ slots_names      → assert_instance_hasattr(kind="slot")
   ├─ slots_values     → assert_mixins_slots_values
   ├─ attribute_names  → assert_instance_hasattr(kind="attribute")
   └─ method_names     → assert_instance_hasattr(kind="method")
```

**Proč dvě oddělené fáze.** První fáze ("shallow") ověřuje **základní
smlouvu** — bez ní nemá smysl pokračovat vůbec (mixin, který nedědí ze
`SimpleMixin`, nebo se ho vůbec nepodaří připojit, nemůže mít žádné
smysluplné sloty/atributy k ověření). Druhá fáze je **opt-in** — každý ze
čtyř parametrů se testuje jen tehdy, pokud ho volající skutečně předal
(`is not UNSET`), takže testovací kód není nucený vypisovat všechny čtyři
kategorie, i když ho zajímá jen jedna.

**Guard clause po první fázi** (`if instance is None: return None`) —
pokud se instance nepodařilo vytvořit, nemá smysl pokoušet se sáhnout na
její sloty/atributy v druhé fázi — to by jen vyvolalo zavádějící
"navazující" chyby (`AttributeError` na `None`) místo jedné jasné,
původní příčiny.

[▲ Nahoru](#-obsah)

---

## `assert_mixin_inheritance` — kontrola dědičnosti

**Parametry:** `subtests`, `mixin_class`, `verbose`, `intro`.

**Návratová hodnota:** `None` (selhání se hlásí přes `pytest.fail`).

**Dvě kontroly, obě uvnitř jednoho `maybe_subtest` bloku:**

```python
if not isinstance(mixin_class, type):
    pytest.fail("...není třída...")

if not issubclass(mixin_class, SimpleMixin):
    pytest.fail("...nedědí ze SimpleMixin...")
```

Nejjednodušší a zároveň nejzákladnější "fail-fast" hranice v celé sadě —
kontroluje jen to, co musí platit **předtím**, než se o mixinu dá vůbec
uvažovat jako o platném stavebním bloku systému: musí to být třída (ne
instance, ne funkce) a musí dědit ze `SimpleMixin`, aby byla kompatibilní
s `_resolve_flat_mixins`/`_verify_mixin_compatibility` (viz
[README_CREATE_INSTANCE.md](README_CREATE_INSTANCE.md#_verify_mixin_compatibility--kompatibilní-matice)).

[▲ Nahoru](#-obsah)

---

## `assert_mixin_instance_creation` — vytvoření a injekce

**Parametry:** `subtests`, `mixin_class`, `test_class`, `mutable`
(výchozí `True`), `verbose`, `intro`.

**Návratová hodnota:** vytvořená instance, nebo `None` při selhání.

**Čtyři kroky, každý ve vlastním `maybe_subtest`:**

1. **`test_class` musí dědit ze `SimpleConstant`** (což pokrývá i
   `SimpleObject`, protože ten sám dědí ze `SimpleConstant` — viz
   [README_SIMPLE_OBJECT.md](README_SIMPLE_OBJECT.md)) — kontrola, že
   volající poslal platný blueprint, ne libovolnou třídu.
2. **`mixin_class` musí dědit ze `SimpleMixin`** — duplicitní s
   `assert_mixin_inheritance`, ale tady je to lokální, samostatná
   kontrola, takže tahle funkce funguje i sama o sobě, ne jen jako
   součást `assert_simple_mixin`.
3. **Skutečná instanciace** — `test_class(mixins=(mixin_class,),
   mutable=mutable)`, obalená v `try/except`. Tohle je moment, kdy se
   reálně spustí celá pipeline z
   [README_CREATE_INSTANCE.md](README_CREATE_INSTANCE.md) (zploštění
   mixinů, validace kompatibility, `class_dict` sestavení, kompilace).
   Jakákoliv výjimka se převede na čitelné `pytest.fail` s uvedeným
   originálním chybovým textem — testovací kód tak nikdy neuvidí syrový
   traceback z hloubky instance builderu, ale rovnou srozumitelnou zprávu.
4. **Kontrola injekce členů** — ověří, že se mixin skutečně "projevil" na
   výsledné instanci (viz níže).

**Krok 4 je nejzajímavější — jak se pozná, co konkrétně mixin přidal:**

```python
base_mixin_attrs = set(dir(SimpleMixin))

mixin_members = {
    name for name in dir(mixin_class)
    if not (name.startswith("__") and name.endswith("__"))
    and name not in base_mixin_attrs
}

missing_members = [name for name in mixin_members if not hasattr(instance, name)]
```

**Odečtení množin** (`dir(mixin_class)` minus `dir(SimpleMixin)`) je
elegantní trik — místo aby test musel předem vědět, co konkrétně mixin
definuje, prostě porovná "co má mixin navíc oproti holé `SimpleMixin`
základně" a ověří, že přesně tahle množina jmen existuje i na výsledné
instanci. Filtr na dunder metody (`startswith("__") and endswith("__")`)
navíc vyřadí systémové Pythoní věci (`__class__`, `__init__` apod.), které
by jinak falešně vypadaly jako "chybějící člen" kvůli tomu, jak dynamické
třídy fungují.

**Tenhle mechanismus je do jisté míry samotestující** — nemusíš do
`assert_simple_mixin` ručně vypisovat `method_names=(...)` pro každou
metodu, kterou mixin definuje; krok 4 to odhalí automaticky pro **cokoliv**
netriviálního, co mixin přidává. Parametry `slots_names`/`attribute_names`/
`method_names` z `assert_simple_mixin` slouží spíš k **explicitní,
cílené** kontrole konkrétních jmen (a hlavně hodnot u `slots_values`), ne
k základní detekci přítomnosti.

[▲ Nahoru](#-obsah)

---

## `assert_instance_hasattr` — obecná brána přítomnosti

**Parametry:** `subtests`, `instance`, `names` (tuple str), `kind` (str —
pro popisky v chybové hlášce), `verbose`, `intro`.

**Návratová hodnota:** `None`.

**Dvoustupňová validace se guard clause mezi kroky:**

```python
# 1. Validace vstupu — names musí být tuple stringů
if not isinstance(names, tuple): pytest.fail(...); is_valid_input = False
for name in names:
    if not isinstance(name, str): pytest.fail(...); is_valid_input = False

if not is_valid_input:
    return  # guard clause

# 2. Kontrola přítomnosti — teprve teď
for name in names:
    if not hasattr(instance, name):
        pytest.fail(f"...Available attributes: {dir(instance)}")
```

Tahle funkce je **znovupoužitelný, obecný stavební blok** — nekontroluje
jen sloty, jen atributy, nebo jen metody; parametr `kind` je čistě
kosmetický (mění text v chybové hlášce: "slot", "attribute", "method"),
ale mechanismus kontroly (`hasattr`) je pro všechny tři případy identický.
Díky tomu `assert_simple_mixin` volá tuhle **jedinou** funkci třikrát (pro
`slots_names`, `attribute_names`, `method_names`), místo aby měla tři
téměř identické, duplicitní implementace.

**Guard clause mezi validací vstupu a kontrolou přítomnosti** je stejný
vzor, jaký znáš z `assert_simple_mixin` samotného — pokud `names` není
platný tuple stringů, nemá smysl iterovat přes něj a volat `hasattr` s
neplatnými jmény, což by generovalo zavádějící navazující chyby.

**`dir(instance)` v chybové hlášce** — když test spadne na chybějící
atribut, hláška rovnou vypíše **kompletní seznam toho, co instance
skutečně má** — šetří čas při debugování, protože není potřeba spouštět
`dir()` ručně v debuggeru.

[▲ Nahoru](#-obsah)

---

## `assert_mixins_slots_values` — kontrola hodnot slotů

**Parametry:** `subtests`, `instance`, `slots_values` (flexibilní formát —
viz níže), `verbose`, `intro`.

**Návratová hodnota:** `None`.

**Tři kroky, každý s vlastní guard clause:**

```python
# 1. Normalizace vstupu — dva podporované tvary
if isinstance(slots_values, tuple) and len(slots_values) == 2 and isinstance(slots_values[0], str):
    normalized = (slots_values,)          # jediný pár: ("slot", hodnota)
elif isinstance(slots_values, tuple):
    normalized = slots_values             # sekvence párů: (("s1", v1), ("s2", v2))
else:
    pytest.fail(...); normalized = None

if normalized is None:
    return  # guard clause

# 2. Validace struktury každého páru
for pair in normalized:
    if not (isinstance(pair, tuple) and len(pair) == 2): pytest.fail(...); return
    name, _ = pair
    if not isinstance(name, str): pytest.fail(...); return

# 3. Skutečná kontrola — přítomnost i hodnota
for name, expected_value in normalized:
    if not hasattr(instance, name): pytest.fail(...)
    actual_value = getattr(instance, name)
    if actual_value != expected_value: pytest.fail(...)
```

**Flexibilní vstupní formát řeší běžný zdroj tření v testech.** Když
mixin definuje jen **jeden** slot, je otravné psát `slots_values=(("moje_slot",
hodnota),)` — vnořený tuple jen kvůli konzistenci s víceprvkovým
případem. Krok 1 tuhle nepohodlnost odstraňuje: pozná podle tvaru
(`len == 2` a první prvek je `str`), jestli jde o jeden pár, nebo o
sekvenci párů, a normalizuje oboje na stejnou vnitřní reprezentaci
(`tuple` tuplů). Tenhle vzor "přijmi obě rozumné podoby vstupu, sjednoť
je hned na začátku" je stejná filozofie jako `_class_name_splitter` →
`create_names` ("split first, normalize later"), jen aplikovaná na
testovací parametr místo na jméno třídy.

**Kontrola hodnoty je až poslední krok, po dvou vrstvách validace
struktury** — nejdřív se musí ověřit, že `slots_values` má vůbec smysluplný
tvar (krok 1), pak že každý pár je skutečně dvouprvkový tuple se string
jménem (krok 2), a teprve pak (krok 3) se zjišťuje, jestli slot **existuje**
a **má správnou hodnotu**. Tohle postupné zužování zajišťuje, že chybová
hláška vždy ukáže na **první, nejzákladnější** problém, ne na matoucí
následek špatně strukturovaného vstupu.

[▲ Nahoru](#-obsah)

---

## Jak to všechno zapadá dohromady

```
assert_simple_mixin(subtests, MyMixin, test_class=MyConstant, slots_values=(("_counter", 0),))
│
├─ assert_mixin_inheritance(MyMixin)
│     → MyMixin musí dědit ze SimpleMixin
│
├─ assert_mixin_instance_creation(MyMixin, MyConstant)
│     → MyConstant(mixins=(MyMixin,)) se skutečně podaří vytvořit
│     → všechny ne-dunder, ne-SimpleMixin členy MyMixin jsou na instanci přítomné
│     → vrací hotovou instanci
│
└─ (protože slots_values není UNSET)
      assert_mixins_slots_values(instance, (("_counter", 0),))
         → instance._counter existuje a rovná se 0
```

Návratová hodnota `assert_simple_mixin` (hotová instance s mixinem) je
záměrně užitečná i **po** doběhnutí všech vestavěných kontrol — testovací
funkce ji může dál použít pro vlastní, doménově specifické asserty
(zavolat metodu mixinu, zkontrolovat chování po mutaci apod.), aniž by
musela znovu ručně opakovat celou instanciační proceduru.

Celá sada dohromady tvoří **jeden, znovupoužitelný nástroj**, kterým se dá
otestovat kterýkoliv z mixinů zmíněných v historii projektu (`NodesTuple`,
`Snapshot`, `NodesDicts`, `Infrastructure`, `Serialization`, a všechny
`others`/`dunders` podkategorie) — stejným jednotným vzorem, bez ohledu na
to, co konkrétní mixin dělá uvnitř.

[▲ Nahoru](#-obsah)
