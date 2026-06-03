from typing import Any, TYPE_CHECKING
# Outers
from ....utils import SimpleObjectLogicError

if TYPE_CHECKING:
    from ...._metadata.SimpleObjectMetadata import SimpleObjectMetadata


# noinspection PyBroadException
class Normalize:
    """
    Mixin pro normalizaci hodnoty na kanonickou podobu.

    Zajišťuje, že hodnota vstupující do systému je validní,
    ošetřuje stavy 'None' a sjednocuje identické hodnoty s defaultem.
    """

    # Atributy dostupné díky metadatům a ostatním mixinům
    meta: 'SimpleObjectMetadata'
    validate: Any

    @classmethod
    def normalize(cls, value: Any, *, process_none: bool = False) -> Any:
        """
        Normalizuje hodnotu. Vrací hodnotu nebo vyvolá SimpleObjectLogicError.

        Pravidla:
        1. Pokud je value None a process_none=True -> vrací default.
        2. Pokud je value None a process_none=False -> vyvolá chybu.
        3. Pokud je value rovna defaultu -> vrací instanci defaultu (šetří paměť).
        4. Ostatní hodnoty jsou validovány a vráceny v původní podobě.
        """
        default_val = cls.meta.default

        # 1. Ošetření chybějící hodnoty (None)
        if value is None:
            if process_none:
                return default_val

            raise SimpleObjectLogicError(
                error_name="MISSING VALUE ERROR",
                value_label="value",
                value=None,
                expected=f"Platná instance typu {cls.meta.value_type} (nikoliv None)",
                problem=f"Třída '{cls.__name__}' vyžaduje konkrétní hodnotu, ale obdržela 'None'.",
                how_to_fix=(
                    "Předejte platnou hodnotu nebo instanci vyžadovaného typu.",
                    "Pokud chcete, aby systém při zadání 'None' automaticky použil výchozí hodnotu, "
                    "nastavte při volání 'process_none=True'."
                ),
                context=f"Fáze normalizace třídy {cls.__name__}",
                exception=ValueError
            )

        # 2. Sjednocení s výchozí hodnotou (Interning/Optimization)
        # Používáme try-except pro případ, že hodnota nepodporuje porovnávání.
        try:
            if value == default_val:
                return default_val
        except Exception:
            # Pokud porovnání selže, ignorujeme to a necháme hodnotu projít standardní validací.
            pass

        # 3. Validace (Typová i uživatelská)
        # Metoda 'validate' buď projde (vrátí True), nebo vyvolá SimpleObjectLogicError.
        cls.validate(value)

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