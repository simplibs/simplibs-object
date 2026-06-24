from typing import Any
# Inners
from .validations import raise_missing_value_error


def normalize(
    cls,
    value: Any,
    *,
    process_none: bool = False
) -> Any:
    """
    Normalizuje hodnotu. Vrací hodnotu nebo vyvolá SimpleLogicError.

    Pravidla:
    1. Pokud je value None a process_none=True -> vrací default.
    2. Pokud je value None a process_none=False -> vyvolá chybu.
    3. Pokud je value rovna defaultu -> vrací instanci defaultu (šetří paměť).
    4. Ostatní hodnoty jsou validovány a vráceny v původní podobě.
    """

    # 1. Ošetření None
    if value is None:

        # 1.1 Vyřízení pokud je None očekáváné
        if process_none:
            return cls.meta.default

        # 1.2 Vyovální výjimky
        raise_missing_value_error(cls)

    # 2. Ošetření situace kdy je hodnota schodná s defaultní
    # noinspection PyBroadException
    try:

        # 2.1 Pokud hodnota odpovídá defaultu - vrací se odkaz na default
        if value == cls.meta.default:
            return cls.meta.default

    # 2.2 Pokud hodnota není porovnatelná - pokračuje se na validaci
    except Exception:
        pass

    # 3. Validace
    cls.validate(value)

    # 4. Případné logování (je-li nastaveno)
    cls._log_outcome(value)

    # 5. Navrácení zvalidvoané hodnoty
    return value


_DESIGN_NOTES = """
# Normalize

## Účel
Tento mixin je "vstupním filtrem" pro data. Jeho úkolem je zajistit, aby zbytek 
systému pracoval již jen s prověřenými a kanonickými daty.

## Logika porovnávání (Equality vs Identity)
V kódu používáme `value == default_val` uvnitř `try-except` bloku. 
Toto řešení jsme zvolili proto, že:
1. **Optimalizace paměti**: Pokud uživatel zadá hodnotu, která je logicky stejná 
   jako default, vrátíme mu přímo referenci na `meta.default`. 
2. **Robustnost**: Obalení do `try-except` chrání systém před pádem v případě, 
   že `value` je objekt, který při pokusu o porovnání vyvolá chybu (např. 
   nekompatibilní typy u některých knihoven). V takovém případě prostě 
   bezpečně pokračujeme k validaci.

## Parametr process_none
Tento parametr dává vývojáři explicitní kontrolu nad tím, jak se má systém 
chovat k `None`. Defaultně je `None` nepřípustné (striktní režim), což 
předchází mnoha chybám v runtime.

## Návaznost
Metoda `normalize` interně volá `cls.validate()`, čímž uzavírá řetězec 
bezpečnostních kontrol předtím, než je hodnota uložena do instance.
"""