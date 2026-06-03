from typing import Any, TYPE_CHECKING
# Outers
from ....utils import SimpleObjectLogicError

if TYPE_CHECKING:
    from ...._metadata.SimpleObjectMetadata import SimpleObjectMetadata


class Validate:
    """
    Mixin pro orchestraci kompletního validačního řetězce.

    Propojuje základní typovou kontrolu s doplňkovou uživatelskou
    logikou definovanou v metodě '_validate'.
    """

    # Atributy budou dostupné díky SimpleObjectMeta a ostatním mixinům
    meta: 'SimpleObjectMetadata'
    validate_type: Any
    _validate: Any

    @classmethod
    def validate(cls, value: Any, *, return_bool: bool = False) -> bool:
        """
        Provede kompletní validační řetězec. Vrací True, False nebo vyvolá výjimku.

        Řetězec se skládá z:
        1. Typové validace (ValidateType.validate_type)
        2. Uživatelské validace (definované v _validate)
        """

        # 1. Typová validace
        # Pokud typ nesedí, metoda buď vrátí False, nebo vyvolá výjimku hned zde.
        if cls.validate_type(value, return_bool=return_bool) is False:
            return False

        # 2. Obsahová/Uživatelská validace (custom _validate)
        try:
            # 2.1 Voláme uživatelskou metodu. Metadata garantují její signaturu.
            if cls._validate(value, return_bool=return_bool) is False:
                return False

        except Exception as e:
            # 2.2 Pokud je vyžadován pouze boolean, potlačíme jakoukoliv chybu a vracíme False
            if return_bool:
                return False

            # 2.3 Pokud jde o naši známou výjimku (LogicError nebo MetadataError),
            # necháme ji "letět" dál beze změny, protože už má správný formát.
            if isinstance(e, SimpleObjectLogicError):
                raise

            # 2.4 Cizí nebo neočekávané výjimky obalíme do našeho standardu,
            # abychom zachovali jednotný formát chybových hlášení.
            raise SimpleObjectLogicError(
                error_name="VALIDATION ERROR",
                value_label="value",
                value=value,
                expected="Hodnota splňující podmínky metody '_validate'",
                problem=f"Během interní validace třídy '{cls.__name__}' došlo k neočekávané chybě.",
                how_to_fix=(
                    "Pro vyvolávání chyb v '_validate' používejte 'SimpleObjectLogicError' "
                    "nebo pomocnou metodu 'cls.bool_or_raise_exception()'.",
                    "Pokud vyvoláváte výjimku manuálně, respektujte parametr 'return_bool'.",
                    "Prověřte implementaci své metody '_validate' (např. zda neobsahuje KeyError, AttributeError).",
                    "Zkontrolujte, zda vstupní data odpovídají předpokladům vaší validační logiky."
                ),
                exception=type(e)
            )

        # 3. Navrácení True pro potvrzení úspěšné validace
        return True


_DESIGN_NOTES = """
# Validate

## Účel
Tento mixin je hlavním orchestrátorem validace. Zajišťuje, že žádná hodnota 
nevstoupí do systému, aniž by prošla oběma úrovněmi kontroly (typ i obsah).

## Logika Try-Except bloku
Blok `try-except` kolem `_validate` je zde ze dvou kritických důvodů:
1. **Unifikace výstupu**: Uživatelé mohou psát `_validate` různými způsoby. 
   Někdo vrací `bool`, někdo jen vyhazuje výjimky. Tento blok garantuje, 
   že pokud je nastaveno `return_bool=True`, metoda `validate` vždy vrátí 
   čisté `False`, i kdyby v `_validate` nastala fatální chyba.
2. **Obalení "cizích" chyb**: Pokud v uživatelské validaci dojde k chybě, 
   kterou autor neošetřil (např. indexace mimo rozsah), systém ji zachytí 
   a prezentuje ji v rámci standardního `SimpleObjectLogicError` formátu, 
   což udržuje konzistenci tracebacku a UI hlášení.

## Pořadí operací
Typová kontrola (`validate_type`) běží vždy jako první. Je to "levná" operace 
v porovnání s potenciálně složitou logikou v `_validate` a slouží jako 
nezbytný předpoklad pro to, aby uživatelský kód v `_validate` mohl 
s hodnotou bezpečně pracovat.
"""