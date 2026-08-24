# 🔗 `value` property — Jednotný přístup k hodnotě

Property `value` je **jediné veřejné rozhraní**, přes které uživatel čte
i zapisuje hodnotu — ať jde o kořenovou instanci, nebo o libovolně
zanořený vnitřní prvek uvnitř kompozice. Tenhle dokument popisuje
mechaniku, která tohle jednotné rozhraní staví.

---

## 🧭 Obsah

* [`create_value_property` — sestavení property](#create_value_property--sestavení-property)
* [`create_value_getter` — čtení](#create_value_getter--čtení)
* [`create_value_setter` — zápis](#create_value_setter--zápis)
* [`create_instance_property` — přístup k instanci, ne k hodnotě](#create_instance_property--přístup-k-instanci-ne-k-hodnotě)
* [`create_properties_for_inner` — obě dohromady pro jeden prvek](#create_properties_for_inner--obě-dohromady-pro-jeden-prvek)

---

## `create_value_property` — sestavení property

**Parametry:**
* `meta`: metadata prvku, ke kterému property patří.
* `is_constant` (*bool*, výchozí `True`): atomické, nebo kompozitní chování setteru.
* `mutable` (*bool*, výchozí `True`): jestli se má vůbec vytvářet setter.
* `path` (*tuple | None*): `None` pro kořenovou hodnotu, jinak cesta ke
  vnitřnímu prvku.

**Návratová hodnota:** `property` objekt s vygenerovaným docstringem.

```python
def create_value_property(meta, *, is_constant=True, mutable=True, path=None):
    getter = create_value_getter(meta, path)

    if not mutable:
        return property(fget=getter, doc=...)

    setter = create_value_setter(meta, is_constant, path)
    return property(fget=getter, fset=setter, doc=...)
```

**Immutable → jen getter.** Pokud je instance immutable, `property` se
vůbec nesestaví se setterem — pokus o zápis (`instance.value = ...`)
selže na úrovni Pythonu samotného (`AttributeError: can't set attribute`),
ne na nějaké vlastní validaci. Nejsilnější možná garance immutability —
zápis prostě neexistuje.

**Automaticky generovaný docstring** se liší podle `is_constant` — u
atomu popisuje normalizaci a bublání nahoru, u kompozice popisuje
dekompozici a distribuci do vnitřních prvků. Díky tomu `help(MyClass.value)`
dá uživateli rovnou smysluplný, kontextově správný popis, i když je celá
property vygenerovaná dynamicky.

**Tahle funkce vytváří `value` pro dvě různé věci zároveň** — kořenovou
hodnotu instance (`path=None`, volaná z `make_atom_class`/`make_composite_class`)
i hodnotu libovolného vnitřního prvku (`path=(...)`, volaná z
`create_properties_for_inner` níže). Je to jeden sjednocený mechanismus,
ne dvě oddělené implementace.

[▲ Nahoru](#-obsah)

---

## `create_value_getter` — čtení

**Parametry:** `meta`, `path` (`None`, nebo tuple).

**Návratová hodnota:** getter funkce.

```python
def create_value_getter(meta, path):
    if path is None:
        def getter(self):
            return self._value
    else:
        get_inner_instance = attrgetter(*path)
        def getter(self):
            return get_inner_instance(self).value

    getter.__annotations__ = {"return": meta.value_type}
    return getter
```

**Getter je záměrně naprosto stejný pro atomy i kompozice** — vždy jen
vrátí aktuální normalizovanou hodnotu. Veškerý rozdíl mezi atomickým a
kompozitním chováním je soustředěný do **setteru** (viz níže); getter
zůstává jednotný a bezstavový.

**`operator.attrgetter(*path)` místo řetězu `getattr`** — pro vnořený
přístup (`path = ("_engine", "_pistons")`) je `attrgetter` rychlejší než
ruční řetězení `getattr` volání a nealokuje mezikroky navíc.

[▲ Nahoru](#-obsah)

---

## `create_value_setter` — zápis

**Parametry:** `meta`, `is_constant` (výchozí `False`), `path` (výchozí `None`).

**Návratová hodnota:** setter funkce.

**Pod kapotou (zkráceně):**
```python
def create_value_setter(meta, is_constant=False, path=None):
    get_inner = attrgetter(*path) if path is not None else None

    def setter(self, value):
        if self._locked:
            raise_locked_value_error(value, self.__class__.__name__)

        if not is_constant and not meta.is_decomposeable:
            raise_class_not_decomposeable(meta)

        instance = get_inner(self) if get_inner is not None else self

        instance._root_value_setter(value, recalculate_up=True)

        if not is_constant:
            instance._recalculate_inners()

        if path is None:
            log_value_event(self.__class__, value, event="set")

    return setter
```

Pět kroků, v přesně tomhle pořadí:

1. **Zámek má vždy přednost.** `self._locked` se kontroluje jako úplně
   první — žádná jiná logika se ani nezačne vyhodnocovat, pokud je
   instance zamčená.
2. **Kompozitní setter vyžaduje dekomponovatelnost.** Pokud jde o
   kompozici (`not is_constant`) a `meta.is_decomposeable` je `False`,
   zápis se rovnou zamítne — nemá smysl přijmout hodnotu, kterou by
   nešlo rozložit do vnitřních prvků.
3. **Rozliš kořen vs. vnitřní prvek** (`instance = get_inner(self) if
   ... else self`) — od teď se pracuje s **cílovou** instancí, ne
   nutně s `self`.
4. **Zápis + případná dekompozice.** Vždy se nejdřív zapíše hodnota přes
   `_root_value_setter(value, recalculate_up=True)` (bublání nahoru
   povolené — tohle je veřejný, uživatelem iniciovaný zápis). Pokud jde o
   kompozici, hned poté se zavolá `_recalculate_inners()`, aby se nová
   hodnota rozdistribuovala dolů do vnitřních prvků.
5. **Logování jen na kořenové úrovni.** `if path is None` — změna
   vnitřního prvku se loguje jen jednou, na úrovni, kde ji uživatel
   skutečně vyvolal, ne opakovaně na každém mezikroku kaskády.

**Tenhle setter je most mezi dvěma reaktivními směry** popsanými
v [README_COMPOSITE_CLASS.md](README_COMPOSITE_CLASS.md#reaktivita-jako-celek) —
krok 4 spouští jak `_recalculate_self` (přes `_root_value_setter` →
bublání), tak `_recalculate_inners` (přímo), podle toho, jestli je cíl
atom, nebo kompozice.

[▲ Nahoru](#-obsah)

---

## `create_instance_property` — přístup k instanci, ne k hodnotě

**Parametry:** `inner_meta`, `path`.

**Návratová hodnota:** read-only `property`.

```python
def create_instance_property(inner_meta, path):
    get_inner_instance = attrgetter(*path)

    def getter(self):
        return get_inner_instance(self)

    return property(fget=getter, doc=...)
```

Strukturální protějšek k `value` property — místo **hodnoty** vnitřního
prvku vrací přímo jeho **instanci** (objekt se svým vlastním `.value`,
`.owner`, případně metodami z mixinů). Vždy jen getter — nahrazení celé
vnitřní instance zvenčí není nikdy povolené, jen nastavení její hodnoty
(přes `value` property).

Tahle property se hodí hlavně pro introspekci a pokročilé použití, kde
uživatel potřebuje sáhnout na vnitřní prvek jako na plnohodnotný objekt
(např. zavolat na něm metodu z mixinu), ne jen přečíst jeho hodnotu.

[▲ Nahoru](#-obsah)

---

## `create_properties_for_inner` — obě dohromady pro jeden prvek

**Parametry:** `inner_meta`, `path` (výchozí `()`), `mutable` (výchozí `True`).

**Návratová hodnota:** `dict` se dvěma klíči.

```python
def create_properties_for_inner(inner_meta, path=(), *, mutable=True):
    name_snake = inner_meta.name_snake
    instance_path = path + (inner_meta.name_private,)

    return {
        name_snake: create_value_property(inner_meta, is_constant=inner_meta.is_constant,
                                            mutable=mutable, path=instance_path),
        f"{name_snake}_instance": create_instance_property(inner_meta, instance_path),
    }
```

Pro jeden vnitřní prvek (řekněme `engine`) vygeneruje **dvě** properties
najednou:

* **`engine`** — hodnota (čtení vždy, zápis podle mutability a
  dekomponovatelnosti).
* **`engine_instance`** — samotná instance (vždy jen ke čtení).

**`instance_path = path + (inner_meta.name_private,)`** — tohle je místo,
kde se skládá cesta pro zanořený přístup. Funkce dostává `path` zvenčí
(volající, typicky `create_properties_for_inners`, předává `()` pro
přímé prvky) a rozšiřuje ji o vlastní privátní slot. Pro vícenásobně
zanořené struktury (kdyby volající předal neprázdnou `path`) by výsledná
cesta rostla o další úroveň — mechanismus je tedy připravený i na hlubší
zanoření, i když v základním případě (`create_properties_for_inners`
volá vždy s `path=()`) se používá jen jedna úroveň.

Výsledný `dict` se pak přímo slučuje (`|=`) do `class_dict` při kompilaci
kompozitní třídy (viz
[README_COMPOSITE_CLASS.md](README_COMPOSITE_CLASS.md#create_properties_for_inners--přístup-k-vnitřním-prvkům)).

[▲ Nahoru](#-obsah)

➡️ Pokračování: [README_INSTANCE_PROTOCOLS.md](README_INSTANCE_PROTOCOLS.md)
