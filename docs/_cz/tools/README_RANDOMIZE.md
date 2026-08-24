# 🎲 Randomize — Fuzzování náhodnými hodnotami

Tenhle dokument popisuje dva nástroje, které propojují `simplibs-object`
s [`simplibs-randomize`](../../../../simplibs-randomize/README.md) —
knihovnou, kterou jsme dokumentovali jako první v pořadí. Zatímco tam šlo
o generování náhodných hodnot samo o sobě, tady se ta samá knihovna
zapojuje **do stromu instancí**, aby uměla vyplnit celou kompozici (nebo
jen jeden atom) validními náhodnými daty — typicky pro testování.

Dva soubory, dvě úrovně:

* **`randomize_value`** — nízkoúrovňový "motor": vygeneruje a přiřadí
  náhodnou hodnotu **jedné konkrétní** listové instanci.
* **`random_data_filler`** — vysokoúrovňový orchestrátor: projde **celý
  strom** instance (kompozice i s vnořenými prvky) a zavolá `randomize_value`
  na každém vhodném místě.

---

## 🧭 Obsah

* [`randomize_value` — jeden list](#randomize_value--jeden-list)
* [`random_data_filler` — celý strom](#random_data_filler--celý-strom)
* [Jak spolu obě funkce souvisí](#jak-spolu-obě-funkce-souvisí)

---

## `randomize_value` — jeden list

**Parametry:**
* `instance` (*SimpleInstanceLike*): cílová instance k naplnění náhodnou hodnotou.
* `retries` (*int*): kolikrát nejvýš zkusit vygenerovat a přiřadit hodnotu.
* `registry` (*RegistryBase | None*): volitelný vlastní registr randomizerů
  (viz [README_LOCAL_REGISTRY.md](README_LOCAL_REGISTRY.md)) — pokud
  `None`, použije se globální `RANDOMIZERS`.
* `skip_unregistered` (*bool*, výchozí `False`): pokud `True`, tiše
  přeskočí typy, pro které není registrovaný žádný randomizer, místo
  vyhození `RandomizeError`.
* `validate` (*bool*, výchozí `True`): zapíná/vypíná kontrolu vstupních parametrů.

**Návratová hodnota:** stejná instance, mutovaná na místě.

**Výjimky:**
* `SimpleRuntimeError` — neplatné parametry, nebo vyčerpané pokusy (`retries`).
* `RandomizeError` — typ hodnoty není registrovaný a `skip_unregistered=False`.

**Pod kapotou (zkráceně):**
```python
def randomize_value(instance, *, retries, registry, skip_unregistered=False, validate=True):
    ...
    value_randomizer = registry.randomize if registry else randomize

    for _ in range(retries):
        try:
            value_type = instance.meta.value_type
            new_value = value_randomizer(value_type)
        except RandomizeError:
            if skip_unregistered:
                return instance
            raise

        if new_value == instance.value:
            continue

        try:
            instance.value = new_value
            return instance
        except Exception:
            continue

    raise_random_data_filler_exhausted(instance, retries)
```

**Čtyři vrstvy odolnosti v jedné smyčce:**

1. **Registr je zaměnitelný** — `registry.randomize if registry else
   randomize` — funkce je stejně dobře použitelná s globálním registrem i
   s izolovaným `LocalRegistry`, díky čemuž fuzzování jde omezit na
   předvídatelnou množinu hodnot (např. v testech).
2. **Nezaregistrovaný typ se dá buď ignorovat, nebo nahlásit** — chování
   řídí `skip_unregistered`. V kontextu stromu kompozic (viz
   `random_data_filler` níže) dává smysl typicky "ignorovat", protože ne
   každý typ v systému musí mít vlastní randomizer.
3. **Odmítnutí identické hodnoty** (`if new_value == instance.value:
   continue`) — funkce garantuje, že hodnota se **skutečně změní**, ne že
   jen "zkusí" a případně vrátí to samé.
4. **Odchycení validačních chyb ze setteru** (`except Exception: continue`)
   — vygenerovaná náhodná hodnota může projít typovou kontrolou
   randomizeru, ale přesto neprojít **doménovou** validací (`_validate`)
   dané instance. Setter to odhalí a smyčka to bere jako "zkus to znovu",
   ne jako fatální chybu — dokud se nevyčerpají `retries`.

**Proč `raise_random_data_filler_exhausted` na konci, ne tiché selhání** —
pokud se ani po `retries` pokusech nepodaří najít validní odlišnou hodnotu,
je to signál, že buď je `retries` nastavené příliš nízko, nebo je doménová
validace natolik striktní, že náhodné hodnoty daného typu skoro nikdy
neprojdou — v obou případech je lepší o tom vědět hned, ne mít tiše
nezměněnou hodnotu.

[▲ Nahoru](#-obsah)

---

## `random_data_filler` — celý strom

**Parametry:**
* `instance` (*SimpleInstanceLike*): kořen stromu (atom, nebo kompozice) k naplnění.
* `retries` (*int*, výchozí `5`): limit pokusů na **každý** list zvlášť.
* `registry` (*RegistryBase | None*, výchozí `None`).
* `skip_unregistered` (*bool*, výchozí `False`).
* `skip_immutable` (*bool*, výchozí `True`): přeskočí zamčené/immutable
  instance místo pokusu o mutaci.
* `validate` (*bool*, výchozí `True`).

**Návratová hodnota:** stejná kořenová instance, mutovaná na místě (celý
podstrom, ne jen kořen).

**Pod kapotou (zkráceně):**
```python
def random_data_filler(instance, *, retries=5, registry=None,
                        skip_unregistered=False, skip_immutable=True, validate=True):
    ...
    is_immutable = not getattr(instance, "__is_mutable__", True)
    is_locked = getattr(instance, "_locked", False)
    if skip_immutable and (is_immutable or is_locked):
        return instance

    if instance.meta.is_constant or instance.meta.is_decomposeable:
        randomize_value(instance, retries=retries, registry=registry,
                         skip_unregistered=skip_unregistered, validate=False)

    if hasattr(instance.meta, "inners"):
        for inner in instance.meta.inners:
            inner_instance = getattr(instance, inner.meta.name_private)
            random_data_filler(inner_instance, retries=retries, registry=registry,
                                skip_unregistered=skip_unregistered,
                                skip_immutable=skip_immutable, validate=False)

    return instance
```

**Rekurzivní procházení stromu s dvěma nezávislými akcemi na každém
uzlu** — tohle je klíčová myšlenka celé funkce:

1. **Přímé přiřazení** (krok "Top-Down") — pokud je uzel buď atom
   (`is_constant`), nebo dekomponovatelná kompozice (`is_decomposeable`),
   zavolá se na něm rovnou `randomize_value`. U dekomponovatelné kompozice
   to znamená vygenerovat náhodnou hodnotu **celé kompozice najednou** a
   nechat `_recalculate_inners` (viz
   [README_COMPOSITE_CLASS.md](README_COMPOSITE_CLASS.md#create_recalculate_inners--tok-hodnot-dolů)),
   aby ji rozdistribuovalo dolů do vnitřních prvků — tím se otestuje
   **shora dolů** propagace.
2. **Rekurze do dětí** (krok "Bottom-Up") — bez ohledu na to, jestli krok 1
   proběhl, funkce projde `instance.meta.inners` (pokud existují) a
   zavolá se rekurzivně na každém vnitřním prvku. Protože vnitřní prvky
   při svém vlastním náhodném přiřazení bublají zpátky nahoru přes
   `_recalculate_self`, tím se otestuje i **zdola nahoru** propagace.

Kombinace obou kroků znamená, že `random_data_filler` neúmyslně slouží i
jako **reaktivní stress test** — jediné zavolání funkce na kořeni prochází
a cvičí oba směry reaktivity popsané v
[README_COMPOSITE_CLASS.md](README_COMPOSITE_CLASS.md#reaktivita-jako-celek).

**Ochrana proti mutaci zamčeného/immutable stavu** je první věc, která se
zkontroluje na každém uzlu (`skip_immutable and (is_immutable or
is_locked)`) — díky `getattr(..., True)`/`getattr(..., False)` s
bezpečnými defaulty funkce nespadne, ani kdyby narazila na instanci bez
těchto atributů.

**`validate=False` ve všech rekurzivních/navazujících voláních** — validace
vstupních parametrů (typ `instance`, `retries > 0`...) se provede jen
jednou, na úrovni prvního volání uživatelem. Všechna následná volání (ať
už `randomize_value` uvnitř, nebo rekurzivní volání sebe sama) ji vypínají
— parametry se v rekurzi nemění, takže opakovaná validace by byla čistě
zbytečná režie.

[▲ Nahoru](#-obsah)

---

## Jak spolu obě funkce souvisí

```
random_data_filler(root)
│
├─ root.meta.is_constant / is_decomposeable?
│    └─ randomize_value(root, ...)          ← vygeneruje a přiřadí 1 hodnotu
│
└─ pro každý root.meta.inners:
     └─ random_data_filler(inner_instance)  ← rekurze, stejný vzor znovu
```

`randomize_value` nikdy neví nic o stromové struktuře — pracuje jen s
jednou instancí. `random_data_filler` naopak nikdy negeneruje hodnoty
sám — deleguje veškerou práci s randomizery na `randomize_value` a stará
se výhradně o **procházení a rozhodování, kde se má co zavolat**. Tohle
rozdělení odpovědností je stejný vzor jako jinde v knihovně (např.
`calculate_value` vs. `_process_calculate_value_params`) — jedna funkce
"co", druhá "kde/jak často".

[▲ Nahoru](#-obsah)
