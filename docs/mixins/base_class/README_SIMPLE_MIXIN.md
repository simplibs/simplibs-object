# 🧱 `SimpleMixin` — Základ pro tvorbu vlastních mixinů

`SimpleMixin` je kořenová třída, ze které musí dědit **úplně každý**
mixin v Simple systému. Sama o sobě nedělá nic funkčního — jejím úkolem
je dát mixinům společnou identitu, deklarativní kompatibilní příznaky a
hlavně **přísnou strukturální validaci při definici**, protože mixiny se
(narozdíl od běžné Pythoní dědičnosti) injektují přímo do `class_dict`
dynamicky vytvářených instančních tříd (viz
[README_CREATE_INSTANCE.md](README_CREATE_INSTANCE.md#_build_instance_class_dict--namespace-injection)) —
jakákoliv strukturální chyba by se tam propsala nebezpečně a nečitelně.

```
SimpleMixin (metaclass=SimpleMixinMeta)
├── NodesTuple, NodesDicts, Snapshot, ...   (core_mixins)
└── tvůj vlastní mixin
```

---

## 🧭 Obsah

* [Deklarativní kompatibilní příznaky](#deklarativní-kompatibilní-příznaky)
* [`__slots__` a `init_mixins`](#__slots__-a-init_mixins)
* [`SimpleMixinMeta` — validace při definici, identita za běhu](#simplemixinmeta--validace-při-definici-identita-za-běhu)
* [`_verify_mixin_definition` — co všechno se kontroluje](#_verify_mixin_definition--co-všechno-se-kontroluje)

---

## Deklarativní kompatibilní příznaky

```python
class SimpleMixin(metaclass=SimpleMixinMeta):
    _constant_only: bool = False
    _composite_only: bool = False
    _mutable_only: bool = False
    _immutable_only: bool = False
    _only_types: "ValidTypes" = UNSET

    __slots__ = ()

    def init_mixins(self) -> None:
        pass
```

Pět příznaků, které vlastní mixin může přepsat, aby deklaroval, na jaké
instance se smí připojit — přesně ty, které `_verify_mixin_compatibility`
skutečně vynucuje při každém vytváření instance (viz
[README_CREATE_INSTANCE.md](README_CREATE_INSTANCE.md#_verify_mixin_compatibility--kompatibilní-matice)):

| Příznak | Omezuje na |
|---|---|
| `_constant_only` | jen atomické instance |
| `_composite_only` | jen kompozitní instance |
| `_mutable_only` | jen mutable instance |
| `_immutable_only` | jen immutable instance |
| `_only_types` | jen instance, jejichž `meta.default` odpovídá danému typu/union |

**Výchozí hodnoty jsou vždy "bez omezení"** (`False`/`UNSET`) — mixin,
který žádný příznak nepřepíše, jde připojit kamkoliv. To je přesně důvod,
proč `TestMixin` (viz
[README_BULK_TEST.md](README_BULK_TEST.md#testmixin--syntetický-testovací-dvojník))
nechává všechny příznaky na výchozích hodnotách — potřebuje fungovat
univerzálně.

[▲ Nahoru](#-obsah)

---

## `__slots__` a `init_mixins`

**`__slots__ = ()`** na `SimpleMixin` samotné je jen výchozí hodnota — ve
skutečnosti musí **každý konkrétní mixin** definovat svoje vlastní
`__slots__` explicitně, i kdyby byly prázdné. Tohle není jen konvence,
je to **vynucené** validací (viz
[`_verify_mixin_definition`](#_verify_mixin_definition--co-všechno-se-kontroluje)
níže) — bez explicitního `__slots__` mixin vůbec neprojde definicí.

**`init_mixins` je izolovaný hook, ne řetězec přes `super()`.** Docstring
na metodě to říká přímo: mixin, který `init_mixins` přepíše, **nesmí**
volat `super().init_mixins()`. Důvod je architektonický — mixiny se
neskládají přes MRO, takže `super()` řetězení by tu nedávalo smysl (a ani
by fungovat nemohlo spolehlivě). Místo toho instance builder sesbírá
`init_mixins` ze všech mixinů zvlášť a sám je zřetězí do jedné funkce
(`_build_combined_init_mixins`, viz
[README_CREATE_INSTANCE.md](README_CREATE_INSTANCE.md#_build_combined_init_mixins--řetězení-inicializace)).
Tvůj mixin tedy má psát `init_mixins` tak, jako by byl **jediný** mixin na
světě — nastavit jen svoje vlastní sloty, nic víc.

[▲ Nahoru](#-obsah)

---

## `SimpleMixinMeta` — validace při definici, identita za běhu

Metaclass `SimpleMixin` řeší dvě nezávislé věci.

### 1. Validace při definici (`__init__`)

```python
def __init__(cls, name, bases, dct, **kwargs):
    super().__init__(name, bases, dct, **kwargs)
    if bases:
        _verify_mixin_definition(cls)
```

**`if bases:`** — jednořádková, ale důležitá podmínka. `SimpleMixin`
samotná má prázdný `bases` tuple (nedědí z ničeho kromě `object`), takže
by na sobě samotné validaci spustit nešlo (a ani nemá smysl — je to
kořen, ne konkrétní mixin). Každá **odvozená** třída (`bases` není
prázdný) projde validací okamžitě při definici — **fail-fast** princip:
chybně definovaný mixin nikdy nedostane šanci proniknout hlouběji do
systému a selhat až později, nečitelně, uprostřed kompilace nějaké
konkrétní instance.

### 2. Identita za běhu (`__instancecheck__`)

```python
def __instancecheck__(cls, instance):
    if super().__instancecheck__(instance):
        return True
    mixins = getattr(instance, "__mixins__", ())
    return any(issubclass(m, cls) for m in mixins)
```

Tohle řeší konkrétní problém: protože mixiny **nejsou** v MRO výsledné
instanční třídy (jsou zploštěné do `class_dict`, viz
[README_CREATE_INSTANCE.md](README_CREATE_INSTANCE.md#create_instance_class--kompilace-finální-třídy)),
běžné `isinstance(obj, MyMixin)` by bez tohohle přepsání **vždy vrátilo
`False`** — Python by hledal `MyMixin` v MRO a nenašel by ji tam.

Řešení je dvoukrokové: napřed zkusit standardní MRO kontrolu (`super()...`,
pro jistotu, kdyby někdy mixin byl přece jen přímo v MRO), a pokud
neuspěje, sáhnout na `instance.__mixins__` — plochý tuple všech mixinů,
který `_build_instance_class_dict` uložil na třídu (viz
[README_CREATE_INSTANCE.md](README_CREATE_INSTANCE.md#_build_instance_class_dict--namespace-injection)) —
a zkontrolovat, jestli je tam `cls` sama, nebo některá její podtřída
(`issubclass(m, cls)`). Díky tomu `isinstance(instance, Snapshot)` funguje
přesně tak, jak by uživatel intuitivně čekal, i když je to technicky
"podvod" oproti standardnímu Pythoní mechanismu.

[▲ Nahoru](#-obsah)

---

## `_verify_mixin_definition` — co všechno se kontroluje

Devět kroků, spuštěných jednou při definici každého konkrétního mixinu:

```
1. __slots__ MUSÍ být v cls.__dict__ (explicitně definované, ne zděděné)
2. slots MUSÍ být tuple nebo str
3. všechny položky slots MUSÍ být str
4. slots NESMÍ obsahovat zakázaná jména (FORBIDDEN_NAMES)
5. class-level namespace NESMÍ obsahovat zakázaná jména
6. kompatibilní příznaky (RESTRICTION_FLAGS) MUSÍ být bool, pokud jsou definované
7. _only_types MUSÍ mít jednu z podporovaných forem (UNSET / type / tuple[type] / Union)
8. init_mixins NESMÍ volat super() (kontrola přes bytecode co_names)
```

**Krok 1 je nejpřísnější a nejdůležitější** — bez explicitního `__slots__`
mixin vůbec neprojde. Tohle vynucuje to, co bylo zmíněno výše: každý
mixin musí sám deklarovat svůj paměťový layout, jinak by hrozilo, že se
mixinu omylem vytvoří `__dict__` (a tím i neomezené, nekontrolované
přidávání atributů, které by rozbilo garance zbytku systému o
předvídatelném layoutu instance).

**Kroky 4–5 (zakázaná jména) chrání interní API systému.** `FORBIDDEN_NAMES`
obsahuje jména, která už mají v systému svůj vlastní, pevně daný význam
(např. `_value`, `_owner`, `value`, `meta`, `init_mixins` jako override
by tu byl výjimkou z výjimky — pozor, `init_mixins` je legitimní
přepsatelný hook, `FORBIDDEN_NAMES` chrání spíš interní strukturální
atributy jako `_value`/`_owner`/`_locked`). Kdyby mixin definoval slot
nebo atribut se stejným jménem, došlo by k **tiché kolizi** — mixinův
atribut by buď přepsal, nebo byl přepsán systémovým, bez jakéhokoliv
varování za běhu. Validace to odhalí hned, srozumitelně, při definici.

**Krok 8 je jediná kontrola, která čte přímo bytecode** (`func.__code__.co_names`)
místo AST nebo stringového hledání — rychlá, spolehlivá detekce, jestli
funkce `init_mixins` **kdekoliv** uvnitř sebe odkazuje na jméno `super`.
Tahle kontrola je přímým vynucením pravidla popsaného výše ("bez
`super()` řetězení") — bez ní by chybné volání `super().init_mixins()`
mohlo vést k matoucímu `AttributeError` až za běhu, hluboko v instance
builderu, místo jasné chyby hned při definici mixinu.

[▲ Nahoru](#-obsah)

➡️ Pokračování: [README_WITH_CONSTANT.md](README_WITH_CONSTANT.md)
