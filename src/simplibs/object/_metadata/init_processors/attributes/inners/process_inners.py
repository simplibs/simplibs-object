from simplibs.sentinels import UNSET
from typing import Type
# Outers
from ....._types import SimpleMetaType, SimpleClassType
# Inners
from .validations.inners import (
    validate_inners_is_not_empty,
    validate_inners_is_defined,
    validate_inners_is_tuple
)
from .validations.inner import (
    validate_inner_is_simple_subclass,
    validate_inner_is_not_simple_class,
    validate_inner_is_class
)
from .validations.name_collisions import (
    validate_collision_within_inners,
    validate_if_collision_with_owner_class
)


def process_inners(
    used_names: set,
    name_snake: str,
    owner_class: SimpleClassType,
) -> tuple:
    """
    Validates and processes the list of inner elements (inners) of a composite class.

    Inners determine whether the class behaves as a constant (no inners) or as a
    composition (with inners). This ensures a consistent interface across all classes.

    Args:
        used_names (set): Set of names already registered in the parent hierarchy.
        name_snake (str): Snake_case name of the owner class.
        owner_class (SimpleMetaType): The class being processed.

    Returns:
        tuple: A 5-tuple containing:
            - raw_inners (tuple): Original inner classes
            - new_used_names (set): Updated set of all used names
            - inners_params_name (tuple): Names for the _logic method parameters
            - inners_default (dict): {name: default_value} for default computation
            - inners_annotations (dict): {name: type} for type hints
    """

    # 1. Získání atributu
    raw_inners = getattr(owner_class, "_inners", UNSET)

    # 2. Ověření zda je nově dafinován
    need_validations = "_inners" in owner_class.__dict__ and raw_inners is not UNSET

    # 3. Základní validace
    if need_validations:

        # 3.1 Validace formátu
        if (not raw_inners or
            not isinstance(raw_inners, tuple)):
            validate_inners_is_defined(raw_inners, owner_class)
            validate_inners_is_tuple(raw_inners, owner_class)
            validate_inners_is_not_empty(raw_inners, owner_class)

    # 4. Prepare data containers
    new_used_names = used_names.copy()

    # 5. Main iteration through inners
    for inner in raw_inners:
        inner: SimpleClassType  # Přetypování pro PyCharm

        # 5.1 Base validations: type, subclass, and not base class
        if need_validations:
            from .....SimpleConstant import SimpleConstant
            from .....SimpleObject import SimpleObject
            if (not isinstance(inner, type) or
                not issubclass(inner, SimpleConstant) or
                inner is SimpleConstant or
                inner is SimpleObject):
                validate_inner_is_class(inner, raw_inners, owner_class)
                validate_inner_is_simple_subclass(inner, owner_class)
                validate_inner_is_not_simple_class(inner, owner_class)

        # 5.2 Check for name collisions with parent and siblings
        used_name_collisions = new_used_names & inner.meta.used_names
        if used_name_collisions:
            collision_name = next(iter(used_name_collisions))
            validate_if_collision_with_owner_class(collision_name, name_snake, inner, owner_class)
            if need_validations:
                validate_collision_within_inners(collision_name, name_snake, raw_inners, inner, owner_class)

        # 5.3 Register inner's names into the global namespace
        new_used_names.update(inner.meta.used_names)

    # 6. Return computed values
    return (
        raw_inners,
        new_used_names,
    )


_DESIGN_NOTES = """
# process_inners

## Účel
Validuje a zpracovává seznam vnitřních prvků (inners) kompozitní třídy.
Inners určují, zda se třída chová jako konstanta (bez inners) nebo jako kompozice (s inners).
Tímto přístupem se zajišťuje konzistentní rozhraní a determinismus výpočtů.

## Klíčová roles inners
Inners mohou být výhradně třídy dědící z SimpleConstant (včetně SimpleObject).
To zaručuje, že každý prvek má:
  - Konzistentní metadata (__metadata__)
  - Definovanou typovou anotaci (_type)
  - Výchozí hodnotu (_default)
  - Jmenný prostor (used_names)

Pokud se inners definují, třída je klasifikována jako SimpleObject (kompozice).
Bez inners je třída SimpleConstant (atom).

## Tok zpracování

### 1. Natažení a validace inners
Nejprve se pokusíme natáhnout `_inners` z `__dict__` třídy.
Následuje triple validace:
  - Existuje atribut `_inners`?
  - Je typu tuple?
  - Není prázdný tuple?

Prázdný tuple je chyba, protože by se třída měla chovat jako konstanta (bez inners).

### 2. Příprava kontejnerů
Vytvoří se 4 kontejnery pro sběr dat během iterace:
  - `new_used_names` (set): Akumulátor jmen (kopie původního setu)
  - `inners_params_name` (list): Jména pro parametry metody _logic
  - `inners_default` (dict): Výchozí hodnoty pro výpočet defaultu
  - `inners_annotations` (dict): Typové anotace pro type hints

### 3. Import SimpleConstant a SimpleObject
Třídy se importují až zde (ne na začátku souboru) kvůli circular dependency.
Pokud první dvě validace (4.1) selžou, tyto importy nejsou vykonány,
což šetří CPU cykly v error path.

### 4. Iterace skrze inners
Pro každý inner se provádí:

#### 4.1 Základní validace
Kontroluje se na třech úrovních:
  - `not isinstance(inner, type)` – Pokud to není třída, vrh výjimku
  - `not issubclass(inner, SimpleConstant)` – Pokud to není potomek SimpleConstant, vrh výjimku
  - `inner is SimpleConstant` – Pokud je to přesně SimpleConstant (base class), vrh výjimku
  - `inner is SimpleObject` – Pokud je to přesně SimpleObject (base class), vrh výjimku

Důvod: Pouze uživatelsky definované třídy jsou povoleny, ne samotné bazové třídy.

#### 4.2 Detekce kolizí jmen
Kontroluje se průnik mezi `new_used_names` a `inner.meta.used_names`.
Pokud je průnik neprázdný, vrh specifickou výjimku:
  - Nejprve se zkontroluje zda kolize není způsobena vlastní třídou (collision with owner)
  - Pak se hledá konkrétní inner, který koliduje (collision within siblings)

Tento přístup poskytuje lepší error messages.

#### 4.3 Registrace jmen
Přidá se `inner.meta.used_names` do globálního setu `new_used_names`.
Tímto se zajistí, že všechny vnitřní prvky (i vnořené) jsou v namespace zaregistrovány.

#### 4.4 Sběr metadat
Z každého inner se extrahu:
  - `name_snake` – Název pro parametr _logic
  - `meta.default` – Výchozí hodnota (použije se později v process_default)
  - `meta.value_type` – Typová anotace (použije se v _logic signature)

## Návratová hodnota
Funkce vrací tuple pěti hodnot:
  - `raw_inners` – Původní tuple tříd (pro pozdější reference)
  - `new_used_names` – Aktualizovaný set všech jmen (pro detekci kolizí v composite)
  - `inners_params_name` – Tuple jmen (pro _logic signature)
  - `inners_default` – Dict {name: default} (pro výpočet composite default)
  - `inners_annotations` – Dict {name: type} (pro _logic type hints)

## Happy Path
Kód je optimalizován pro happy path, kde validace proběhnou bez problému:
  - Podmínky na začátku (řádky 1) jsou nejčastěji True → branch predictor caches them
  - Pokud happy path selže, všechny ostatní validace se volají v error path (není penalizace)
  - Žádný zbytečný kód v normálním toku

## Poznámky
- `used_names` se zkopíruje na začátku (`.copy()`) aby se nemodifikoval originál
- Import SimpleConstant/SimpleObject je na pozici 3 aby se neuváděl před happy path kontrolou
- Funkcí se používá výhradně v SimpleObjectMetadata._process_user_interface()
- Všechny chyby vedou k vyhození specifické výjimky, ne k defaultnímu chování
"""