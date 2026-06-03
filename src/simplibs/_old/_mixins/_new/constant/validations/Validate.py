from operator import truediv
from typing import Any, Callable, NoReturn
# Outers
from ....._types import MetaType
# inners
from .exceptions.raise_validation_error import raise_validation_error


class Validate:
    """
    Mixin pro orchestraci kompletního validačního řetězce.

    Propojuje základní typovou kontrolu s doplňkovou uživatelskou
    logikou definovanou v metodě '_validate'.
    """

    # Definice používaných prvků
    meta: MetaType
    validate_type: Callable

    @classmethod
    def validate(
        cls,
        value: Any,
        *,
        return_bool: bool = False
    ) -> bool | NoReturn:
        """
        Provede kompletní validační řetězec. Vrací True, False nebo vyvolá výjimku.

        Řetězec se skládá z:
        1. Typové validace (ValidateType.validate_type)
        2. Uživatelské validace (definované v _validate)
        """

        # 1. Validace typu a validační metodou
        try:
            return (
                cls.validate_type(value, return_bool=return_bool) and
                cls.meta.validate(value, return_bool=return_bool)
            )

        # 2. Zpracování výjimek
        except Exception as e:

            # 2.1 Vyřízení pro bool odpověd
            if return_bool:
                return False

            # 2.2 Vyvolání výjimky
            raise_validation_error(cls, value, e)


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