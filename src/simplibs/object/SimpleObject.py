from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from .SimpleConstant import SimpleConstant
from .protocols import LogicSignature, P, R
from ._validations import process_calculate_value_params
# Anotations
if TYPE_CHECKING:
    from .protocols.classes import SimpleClassLike



class SimpleObject(SimpleConstant):
    """
    Základní definiční třída pro definic kompozic.

    Vychází z SimpleConstant a SimpeBase tířdy.
    Slouží jako základ pro vytváření kompozitních objektů.
    """

    # ===================================
    # VNITŘNÍ ROZHRANÍ KOMPOZITNÍ TŘÍDY
    # (definuje uživatel zakládající třídu)
    # ===================================

    #--- Typová anotace hodnoty kterou třída reprezentuje ---#
    # (povinná hodnota pro konstantu i objekt)
    _type: type = UNSET

    #--- Vnitřní prvky třídy ---#
    # (povinný atribut - musí odpovídat paramerů _logic)
    _inners: tuple["SimpleClassLike", ...] = UNSET

    #--- Hlavní metoda pro výpočet hodnoty ---#
    # (povinný prvek - vypočítává default)
    @classmethod
    def _logic(cls, *args, **kwargs) -> Any:
        """Povinná pro kompozici, vrací default pro atomy."""
        return UNSET

    #--- Doplňková metoda pro rozložení hlavní hodnoty ---#
    # (zadává se pouze je-li rozklad potřeba)
    @classmethod
    def _decompose(cls, value: Any) -> Any:
        """Nepovinná, vrací None, pokud rozklad není podporován."""
        return UNSET

    #--- Doplňková logika validace ---#
    # (zadává se pro rozšíření základní validace dle typu)
    @classmethod
    def _validate(cls, value: Any, *, return_bool: bool = False) -> bool | Exception:
        """Nepovinná doplňková validace."""
        return True


    # ===================================
    # VNĚJŠÍ ROZHRANÍ KOMPOZITNÍ TŘÍDY
    # (metody jsou přidány při zpracování metadat)
    # ===================================

    @classmethod
    def calculate_value(cls: LogicSignature[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
        """
        Dynamicky spočítá hodnotu kompozice.
        Díky ParamSpec PyCharm nahlédne do uživatelské metody '_logic'
        a začne vývojáři našeptávat JEJÍ konkrétní parametry!
        """

        # 1. Zpracování předaných parametrů
        params_dict = process_calculate_value_params(cls, *args, **kwargs)

        # 2. Výpočet hodnoty
        outcome = cls.meta.logic(cls, **params_dict)

        # 3. Případné logování (je-li nastaveno)
        cls._log_outcome(outcome)

        # 4. Navrácení výsledku
        return outcome

    @classmethod
    def decompose_value(cls, value: Any) -> Any:
        """Rozloží hlavní hodnotu na vnitřní komponenty."""

        # 1. Validace předané hodnoty
        cls.validate(value)

        # 2. Rozložení předané hodnoty
        # noinspection PyUnresolvedReferences
        outcome = cls.meta.decompose(cls, value)

        # 3. Případné logování (je-li nastaveno)
        cls._log_outcome(outcome)

        # 4. Navrácení výsledku
        return outcome

    # ===================================
    # METOD Y A ATRIBUTY ZDĚDĚNÉ Z PŘEDKŮ
    # (předkové: SimpleConstant, SimpleBase)
    # ===================================

    #--- Defaultní hodnota která se u kompozice dopočítává ---#
    # _default: Any = UNSET

    #--- Základní validace dle typu ---#
    # validate_type(cls, value: Any, *, return_bool: bool = False) -> bool

    #--- Kompletní validace dle typu a doplňkové validační logiky ---#
    # validate(cls, value: Any, *, return_bool: bool = False) -> bool

    #--- Validace nevyvolávající výjimku, ale vracející pouze bool ---#
    # is_valid(cls, value: Any) -> bool

    #--- Normalizační meotda - provede validaci a navrátí hodnotu ---#
    # normalize(cls, value: Any, *, process_none: bool = False) -> Any

    #--- Hook pro případný loger ---#
    # _log_outcome(cls, outcome: Any) -> None
