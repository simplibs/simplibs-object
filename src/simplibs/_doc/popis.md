# SimpleObject – Parametrická knihovna pro dynamickou generaci tříd

## Úvod a motivace

Tato knihovna vznikla z potřeby vytvořit univerzální mechanismus pro práci s parametrickými třídami. Původně jsem si vytvořil jednoduchou knihovnu pro logování s nastavitelnou třídou a všemi jejími parametry. Při návrhu jsem si všiml, že používám podobnou strukturu v jiných parametrových knihovnách, a napadlo mě, zda by se toto dalo zevšeobecnit.

Výsledkem je třída, která slouží jako základ pro vytváření parametrických tříd, které je potom možné používat v různých projektech. Knihovna se postupně rozrostla z pár řádků kódu na solidně velký projekt, který překračuje svůj původní záměr a stává se univerzálním „švýcarským nožem" pro podobné situace.

**Hlavní výhoda:** Místo aby na paměť aplikace zatížilo více různých rozhraní pro různé parametrické třídy, stačí jedno jediné rozhraní – rozhraní třídy `SimpleObject`. Na tomto základě je pak možné stavět nezávislé konstrukce, které mají jednoduchou logiku, protože vycházejí z logiky této jedné třídy.

## Základní princip

Celý projekt je založen na myšlence, že stačí jen pár vstupních údajů, z nichž je možné deterministicky dopočítat vše ostatní, co je třeba.

Třída `SimpleObject` slouží výhradně pro **deklaraci definice tříd** (rozhraní). Na jejím základě se pak vytváří další třídy, které jsou jejími potomky. Tyto třídy lze pak používat pro vytváření instancí a nových objektů prostřednictvím metaprogramování a dynamické generace objektů.

## Rozhraní SimpleObject – Definice pro uživatele

Zde je základní třída se svým rozhraním:

```python
class SimpleObject(
    # Validate method
    IsValid,                # is_valid(cls, value: Any) -> bool
    Normalize,              # normalize(cls, value: Any, *, process_none: bool = False) -> Any
    Validate,               # validate(cls, value: Any, *, return_bool: bool = False) -> bool
    ValidateType,           # validate_type(cls, value: Any, *, return_bool: bool = False) -> bool
    BoolOrRaiseException,   # def bool_or_raise_exception(cls, return_bool: bool = False, **kwargs) -> bool
    # Base method
    CreateValue,            # create_value(cls, **kwargs) -> Any
    DecomposeValue,         # decompose_value(cls, value: Any) -> Dict[str, Any]
    UpdateValue,            # update_value(cls, value: Any, **kwargs) -> Any
    # Utils
    GetOrMakeCacheAttr,     # _get_or_make_cache_attr(cls, cache_attr: str, method_name: str) -> Any
    CreateMixinParameters,  # MIXIN_PARAMS(cls), collect_mixin_parameters(cls)
    # Metadata
    metaclass=SimpleObjectMeta
):

    # ===================================
    # ZÁKLADNÍ ROZHRANÍ DEFINICE TŘÍDY
    # ===================================

    # Defaultní hodnota - Povinná, pokud nejsou definovány inners
    _DEFAULT: ClassVar[Any] = None

    # Typ - Vždy povinný
    _type: ClassVar[Optional[Type]] = None

    # Inners - Definují se pouze, jsou-li potřeba
    _inners: ClassVar[Tuple[SimpleObjectType, ...]] = None

    @classmethod
    def _logic(cls):
        """Povinná pro kompozici, vrací default pro atomy."""
        return cls._DEFAULT

    @classmethod
    def _decompose(cls, value: Any):
        """Nepovinná, vrací None, pokud rozklad není podporován."""
        return None

    @classmethod
    def _validate(cls, value: Any, return_bool: bool = False):
        """Nepovinná doplňková validace."""
        ...

    # ===================================
    # METADATA PRO TŘÍDNÍ ATRIBUTY
    # ===================================

    __metadata__: ClassVar[SimpleObjectMetadata]
```

### Popis prvků rozhraní

**Atributy:**
- **`_DEFAULT`**: Defaultní hodnota – povinná, pokud třída nemá definovány `_inners`. Nemůže být `None`, protože se používá pro výpočet defaultních hodnot v kompozicích.
- **`_type`**: Typ hodnoty – vždy povinný. Určuje, jakého typu má být hodnota, kterou třída a její default reprezentují.
- **`_inners`**: Vnořené třídy – definují se pouze, jsou-li potřeba. Jedná se o jiné třídy založené na `SimpleObject`, které daná třída používá pro výpočet svého defaultu.

**Metody:**
- **`_logic()`**: Povinná pro kompozitní třídy. Používá všechny `inners` v jejich pořadí a vrací hodnotu odpovídající typu `_type`. Pro atomy vrací `_DEFAULT`.
- **`_decompose(value)`**: Nepovinná metoda pro opačný proces než `_logic`. Očekává hodnotu odpovídající `_type` a rozloží ji na hodnoty pro jednotlivé `inners`. Pokud tato metoda není definována, rozklad není podporován.
- **`_validate(value, return_bool)`**: Nepovinná doplňková validace. Umožňuje lépe specifikovat, jaké hodnoty jsou akceptovatelné, a tedy zajistit, aby třída pracovala pouze s validními daty. Není-li definována, předpokládá se, že třída akceptuje všechny hodnoty daného typu.

### Klassifikace tříd

Třídy dělíme na dvě kategorie:

1. **Atomy** – třídy bez definovaných `inners`. Obsahují jednu konkrétní hodnotu daného typu.
2. **Kompozice** – třídy s definovanými `inners`. Skládají se z menších jednotek (atomů nebo dalších kompozic) a jejich default se dopočítá z jejich `inners`.

**Důležité pravidlo:** Všechny prvky v `inners` musí být potomky `SimpleObject` a mít stejné rozhraní.

## Metody nabízené třídou SimpleObject

Třída nabízí následující základní klasní metody:

- **`is_valid(value)`** – Kontroluje, zda je hodnota validní pro danou třídu.
- **`normalize(value, *, process_none=False)`** – Normalizuje hodnotu.
- **`validate_type(value, *, return_bool=False)`** – Validuje typ hodnoty.
- **`validate(value, *, return_bool=False)`** – Validuje hodnotu podle typu a pomocné metody `_validate`.
- **`create_value(**kwargs)`** – Vytváří hodnotu dle metody `_logic` a validace.
- **`decompose_value(value)`** – Dekomponuje hodnotu dle metody `_decompose`.
- **`update_value(value, **kwargs)`** – Mění hodnotu a hodnoty `inners` pomocí `_decompose`.
- **`_get_or_make_cache_attr(cache_attr, method_name)`** – Načítá nebo vytváří cache meta-atributy.
- **`bool_or_raise_exception(return_bool=False, **kwargs)`** – Zkrácení zápisu podmínky `if return_bool: return False else raise Error`. *(Pozn.: Tato metoda je zatím v přezkumu, protože je dostupná i v knihovně simple-exception a není jisté, zda zůstane.)*

**Defenzivní přístup:** Třída je navržena velmi defenzivně jako uzavřený systém pracující pouze se svými potomky. Metadata kontrolují správnost všech parametrů a obsahují rozsáhlé validace, které odhalují chyby ještě před během programu.

## Generování instancí a objektů

Zatímco třída `SimpleObject` slouží k deklaraci definice, praktické použití probíhá prostřednictvím dynamicky generovaných tříd, které ji rozšiřují. Tyto třídy se vytvářejí v následujících vrstvách:

### 1. SimpleCore – Vytvoření hodnoty (`CORE`)

```python
class SimpleCore(SimpleBase):

    @classmethod
    def CORE(cls):
        """Vytvoří mixin"""
        return cls._get_or_make_cache_attr(
            cache_attr="core_class",
            method_name="make_core"
        )

    @classmethod
    def make_core(cls):

        # 1. Definice vnitřních funkcí
        def __init__(self, new_value: Any = None):
            self._value = self.normalize(new_value, process_none=True)

        def getter(self) -> Any:
            return self._value

        def setter(self, new_value: Any) -> None:
            self._value = self.normalize(new_value, process_none=True)

        # 2. Název nové třídy
        class_name = f"{cls.__name__}Atom"

        # 3. Předci třídy
        class_parents = (SimpleBase,)

        # 4. Slovník nové třídy
        class_dict = {
            '__doc__': f"{class_name} – hodnotové jádro pro {cls.meta.name_readable}",
            '__slots__': ("_value",),
            '__init__': __init__,
            'value': property(getter, setter),
        }

        # 5. Vytvoření nové třídy
        core_class = type(class_name, class_parents, class_dict)
        return core_class
```

**Účel:** Vytváří základní atomickou třídu, která nese konkrétní hodnotu v atributu `value`.

### 2. SimpleInstance – Vytvoření instanční třídy (`INSTANCE`)

```python
class SimpleInstance(SimpleCore):

    @classmethod
    def INSTANCE(cls):
        """Vytvoří instance"""
        return cls._get_or_make_cache_attr(
            cache_attr="instance_class",
            method_name="make_atomic_instance"
        )

    @classmethod
    def get_signature(cls):
        return Signature([
            Parameter(
                cls.meta.name_snake,
                Parameter.KEYWORD_ONLY,
                default=None,
                annotation=cls.meta.value_type
            )
        ])

    @classmethod
    def make_atomic_instance(cls):
        """
        Vytvoří atomickou instanci pro tento SimpleObject.
        Tato instance neřeší inners, jen jeden parametr podle attr_name a param_name.
        """

        # Názvy atributů a parametrů
        attr_name = cls.meta.name_private
        param_name = cls.meta.name_snake
        CoreClass = cls.CORE()

        # 1. Definice vnitřních funkcí
        def __init__(self, **kwargs):
            value = kwargs.get(param_name)
            setattr(self, attr_name, CoreClass(value))

            # Předání kwargs dál po MRO řetězci (mixiny)
            super(type(self), self).__init__(**kwargs)

        def getter(self):
            # Vrací celý atomický objekt
            return getattr(self, attr_name)

        def setter(self, value):
            # Nastaví hodnotu do atomu a vyvolá update hook
            getattr(self, attr_name).value = value
            self._on_update()

        # Podpis pro IDE a našeptávače
        __init__.__signature__ = Signature([cls.meta.atom_param_signature])

        # Název nové třídy
        class_name = f"{cls.__name__}Instance"

        # Předci třídy
        class_parents = (InstanceBase,)

        # Slovník nové třídy
        class_dict = {
            '__doc__': f"{class_name} – atomická instance pro {cls.meta.name_readable}",
            '__slots__': (attr_name,),
            '__init__': __init__,
            param_name: property(getter, setter),
        }

        # Vytvoření nové třídy
        instance_class = type(class_name, class_parents, class_dict)
        return instance_class
```

**Účel:** Vytváří instanční třídu, která skrývá atomickou hodnotu v pojmenovaném privátním atributu (odvozený z názvu třídy). Tím se zabezpečuje, aby nemohlo dojít ke konfliktu názvů. Metadata kontrolují, že žádný `inners` nemá stejný název, aby se vyhnuli kolizím atributů.

### 3. SimpleMixin – Vytvoření kompozitní třídy (`MIXIN`)

```python
class SimpleMixin(SimpleInstance):

    @classmethod
    def MIXIN(cls):
        """Vrátí instanční třídu složenou z mixinů všech inners."""
        return cls._get_or_make_cache_attr(
            cache_attr="mixin_class",
            method_name="make_mixin_class"
        )

    @classmethod
    def make_mixin_class(cls):
        """Vytvoří mixin třídu složenou z vlastní mixin a mixinů všech inners."""

        # Pokud není žádný inners (jedná se o atom)
        if not cls.meta.inners:
            return cls.INSTANCE()

        # Složení mixinů všech inners rekurzivně
        inner_classes = tuple(
            inner.MIXIN() for inner in cls.meta.inners
        )

        # Složení signatur
        def __init__(self, **kwargs):
            super(type(self), self).__init__(**kwargs)

        # Podpis pro IDE a našeptávače
        __init__.__signature__ = Signature(cls.MIXIN_PARAMS())

        # Předci: Aktuální instance + všechny inners
        class_parents = (cls.INSTANCE(),) + inner_classes

        # Název nové třídy
        mixin_names = [inner.__name__ for inner in cls.meta.inners]
        class_name = f"{cls.__name__}Mixin({'_'.join(mixin_names)})"

        # Slovník nové třídy
        class_dict = {
            '__doc__': f"Kompozitní mixin třídy {cls.__name__} složená z: {', '.join(mixin_names)}",
            '__slots__': (),
            '__init__': __init__,
        }

        # Vytvoření nové třídy
        mixin_class = type(class_name, class_parents, class_dict)
        return mixin_class
```

**Účel:** Vytváří kompozitní třídu pro třídy s `inners`. Složí vlastní instanci se mixin třídami všech vnořených prvků, čímž vytvoří jednotné rozhraní reprezentující všechny komponenty.

### 4. SimpleObject – Finální objekt (`OBJECT`)

```python
class SimpleObject(SimpleMixin):

    @classmethod
    def OBJECT(cls, *mixins: Any, use_defaults: bool = True, as_atom: bool = None):
        """
        Vrátí koncovou třídu.
        Pokud jsou použity parametry, generuje se třída dynamicky bez trvalého uložení do cache.
        """
        if as_atom is None and not mixins:
            return cls._get_or_make_cache_attr(
                cache_attr="object_class",
                method_name="make_object_class"
            )

        # Pokud uživatel něco specifikoval, vyrobíme to čerstvě
        return cls.make_object_class(*mixins, use_defaults=use_defaults, as_atom=as_atom)

    @classmethod
    def make_object_class(cls, *mixins: Any, use_defaults: bool = True, as_atom: bool = None):
        """Továrna na koncové objekty."""

        # Určení režimu (Atom vs Mixin)
        is_atom = determine_atom_mode(cls, as_atom)

        # Výběr základního kamene
        ObjectBase = cls.INSTANCE() if is_atom else cls.MIXIN()

        # Vyřešíme mixiny skrze orchestrátor
        ObjectMixins = process_mixins(mixins, use_defaults=use_defaults)

        # Předci: Vybraná báze + naše mixiny se schopnostmi
        class_parents = ObjectMixins + (ObjectBase,)

        # Název nové třídy
        class_name = f"{cls.__name__}Object"

        # Slovník nové třídy
        class_dict = {
            '__doc__': f"Koncový objekt {cls.__name__} (Atom: {is_atom}, Mixins: {mixins})",
            '__slots__': (),
        }

        # Vytvoření nové třídy
        object_class = type(class_name, class_parents, class_dict)
        return object_class
```

**Účel:** Vytváří finální objekt. Umožňuje přidávat volitelné mixiny, které rozšiřují schopnosti třídy. Tímto se stává třída „modulární lego" – uživatel si vybírá z předdefinovaných mixinů nebo vytváří vlastní a skládá si tak přesně tu funkcionalitu, kterou potřebuje.

## Struktura mixinů

Knihovna nabízí rozsáhlou sadu předdefinovaných mixinů organizovaných do kategorií:

```
libraries/simple-object/stc/simple_object/_mixins/instance_class/
├── dunders/
│   ├── _not_implemented/
│   │   ├── attributes/
│   │   ├── collections/
│   │   ├── comparison/
│   │   ├── lifecycle/
│   │   ├── protocols/
│   │   └── system/
│   ├── collections/
│   │   ├── atoms/
│   │   ├── Container.py
│   │   ├── Inspectable.py
│   │   ├── Iterable.py
│   │   ├── Mapping.py
│   │   ├── MappingView.py
│   │   ├── MutableMapping.py
│   │   └── Reversible.py
│   ├── comparison/
│   │   ├── atoms/
│   │   ├── Comparable.py
│   │   ├── Equality.py
│   │   └── Orderable.py
│   ├── descriptions/
│   │   ├── atoms/
│   │   ├── Convertible.py
│   │   ├── Formattable.py
│   │   ├── Hashable.py
│   │   ├── Printable.py
│   │   └── Representable.py
│   ├── lifecycle/
│   │   ├── atoms/
│   │   ├── Copyable.py
│   │   ├── Generic.py
│   │   ├── Persistent.py
│   │   └── Serializable.py
│   ├── numeric/
│   │   ├── atoms/
│   │   ├── Arithmetic.py
│   │   ├── Bitwise.py
│   │   ├── Convertible.py
│   │   ├── ExtendedArithmetic.py
│   │   ├── InPlaceNumeric.py
│   │   ├── Integer.py
│   │   └── Numeric.py
│   └── protocols/
│       ├── atoms/
│       ├── Callable.py
│       └── ContextManager.py
├── main_logic/
│   ├── base/
│   │   ├── InstanceBase.py
│   ├── core/
│   │   ├── Logic.py
│   │   ├── Metadata.py
│   │   └── Validate.py
│   ├── introspection/
│   │   ├── DeepValidate.py
│   │   └── Documentation.py
│   ├── mutation/
│   │   └── Mutation.py
│   ├── patterns/
│   │   ├── Chain.py
│   │   ├── Event.py
│   │   └── Observable.py
│   ├── serialization/
│   │   ├── Deserialize.py
│   │   ├── DictSerializer.py
│   │   ├── JsonSerializer.py
│   │   └── Serialize.py
│   ├── state/
│   │   ├── History.py
│   │   ├── Permission.py
│   │   └── State.py
│   └── utilities/
│       └── Randomize.py
```

Uživatelé mohou volit z těchto mixinů a skládat si tak přesně tu funkcionalitu, kterou jejich třída potřebuje.

## Shrnutí

Třída `SimpleObject` je univerzálním nástrojem pro deklaraci a dynamickou generaci parametrických tříd. Umožňuje:

1. **Deklaraci definic** – Uživatel definuje třídu s atributy `_type`, `_default`, `_inners` a metodami `_logic`, `_decompose` a `_validate`.
2. **Automatickou validaci** – Metadata kontrolují správnost všech parametrů ještě před během.
3. **Dynamickou generaci** – Na základě jedné deklarace se automaticky vytvářejí atomické a kompozitní třídy.
4. **Modularitu** – Skrze mixiny je možné jednoduše přidávat různé schopnosti třídám.
5. **Metaprogramování** – Knihovna využívá pokročilé metaprogramování k vytváření tříd za běhu.

Tímto se stává `SimpleObject` silným nástrojem „švýcarský nůž" pro situace, kde je potřeba pracovat s komplexními parametrickými strukturami.

