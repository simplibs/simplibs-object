from typing import Any, Callable
# Outers
from ....._types import MetaType
# Inners
from .exceptions.raise_missing_value_error import raise_missing_value_error



# noinspection PyBroadException
class Normalize:
    """
    Mixin pro normalizaci hodnoty na kanonickou podobu.

    Zajišťuje, že hodnota vstupující do systému je validní,
    ošetřuje stavy 'None' a sjednocuje identické hodnoty s defaultem.
    """

    # Definice používaných prvků
    meta: MetaType
    validate: Callable

    @classmethod
    def normalize(
        cls,
        value: Any,
        *,
        process_none: bool = False
    ) -> Any:
        """
        Normalizuje hodnotu. Vrací hodnotu nebo vyvolá SimpleObjectLogicError.

        Pravidla:
        1. Pokud je value None a process_none=True -> vrací default.
        2. Pokud je value None a process_none=False -> vyvolá chybu.
        3. Pokud je value rovna defaultu -> vrací instanci defaultu (šetří paměť).
        4. Ostatní hodnoty jsou validovány a vráceny v původní podobě.
        """

        # 1. Ošetření None (Pravidla 1 a 2)
        if value is None:

            # 1.1 Vyřízení pokud je None očekáváné
            if process_none:
                return cls.meta.default

            # 1.2 Vyovální výjimky
            raise_missing_value_error(cls)

        # 2. Sjednocení s defaultem (Pravidlo 3)
        try:

            # 2.1 Pokud hodnota odpovídá defaultu - vrací se odkaz na default
            if value == cls.meta.default:
                return cls.meta.default

        # 2.2 Pokud hodnota není porovnatelná - pokračuje se na validaci
        except Exception:
            pass

        # 3. Validace (Pravidlo 4)
        cls.validate(value)

        # 4. Navrácení zvalidvoané hodnoty
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