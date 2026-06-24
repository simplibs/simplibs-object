from typing import Any
from simplibs.sentinels import UNSET
# Inners
from .SimpleBase import SimpleBase
from ._utils.atom_class import (
    validate_type,
    validate,
    normalize,
    bool_or_raise_validate_error
)


class SimpleConstant(SimpleBase):
    """
    Základní definiční třída pro definic konstant

    Vychází z SimpleBase tířdy.
    Slouží jako základ pro SimpleObject třídu.
    """

    # ===================================
    # VNITŘNÍ ROZHRANÍ KONSTANTNÍ TŘÍDY
    # (definuje uživatel zakládající třídu)
    # ===================================

    #--- Typová anotace hodnoty kterou třída reprezentuje ---#
    # (povinná hodnota pro konstantu i objekt)
    _type: type = UNSET

    #--- Defaultní hodnota ---#
    # (zadává se pouze u konstanty, u objektu se dopočítává)
    _default: Any = UNSET

    #--- Doplňková logika validace ---#
    # (zadává se pro rozšíření základní validace dle typu)
    @classmethod
    def _validate(cls, value: Any, *, return_bool: bool = False) -> bool | Exception:
        """Nepovinná doplňková validace."""
        return True

    # ===================================
    # VNĚJŠÍ ROZHRANÍ KONSTANTNÍ TŘÍDY
    # (metody jsou přidány při zpracování metadat)
    # ===================================

    @classmethod
    def validate_type(cls, value: Any, *, return_bool: bool = False) -> bool | None:
        """Provede deterministickou validaci typu na základě metadat třídy."""
        return validate_type(cls, value, return_bool=return_bool)

    @classmethod
    def validate(cls, value: Any, *, return_bool: bool = False) -> bool | None:
        """Provede validaci typu a validaci skrze upřesňující validační metodu."""
        return validate(cls, value, return_bool=return_bool)

    @classmethod
    def is_valid(cls, value: Any) -> bool | None:
        """Vrátí True, pokud hodnota projde kompletní validací, jinak False."""
        return cls.validate(value, return_bool=True)

    @classmethod
    def normalize(cls, value: Any, *, process_none: bool = False) -> Any:
        """Normalizuje hodnotu. Vrací hodnotu nebo vyvolá SimpleLogicError."""
        return normalize(cls, value, process_none=process_none)

    @classmethod
    def bool_or_raise_validate_error(cls, value: Any, problem: str, *, return_bool: bool = False) -> bool:
        """Pomocná metoda pro použití uvnitř uživatelských '_validate'. (Na instanci je odebrána.)"""
        return bool_or_raise_validate_error(cls, value, problem, return_bool=return_bool)

    # ===================================
    # METOD Y A ATRIBUTY ZDĚDĚNÉ Z PŘEDKŮ
    # (předkové: SimpleBase)
    # ===================================

    #--- Hook pro případný loger ---#
    # _log_outcome(cls, outcome: Any) -> None
