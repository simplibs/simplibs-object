from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from .SimpleConstant import SimpleConstant
from .protocols.methods import LogicSignature, P, R
from ._core_logic.object_methods import calculate_value, decompose_value
# Annotations
if TYPE_CHECKING:
    from .protocols.classes import SimpleObjectProtocol
    from .protocols.alias_typings import ValidTypes, InnersTuple



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
    _type: "ValidTypes" = UNSET

    #--- Vnitřní prvky třídy ---#
    # (povinný atribut - musí odpovídat paramerů _logic)
    _inners: "InnersTuple" = UNSET

    #--- Hlavní metoda pro výpočet hodnoty ---#
    # (povinný prvek - vypočítává default)
    @classmethod
    def _logic(
        cls: "SimpleObjectProtocol",
        *args,
        **kwargs
    ) -> Any:
        """Povinná pro kompozici, vrací default pro atomy."""
        return UNSET

    #--- Doplňková metoda pro rozložení hlavní hodnoty ---#
    # (zadává se pouze je-li rozklad potřeba)
    @classmethod
    def _decompose(
        cls: "SimpleObjectProtocol",
        value: Any
    ) -> Any:
        """Nepovinná, vrací None, pokud rozklad není podporován."""
        return UNSET

    #--- Doplňková logika validace ---#
    # (zadává se pro rozšíření základní validace dle typu)
    @classmethod
    def _validate(
        cls: "SimpleObjectProtocol",
        value: Any,
        *,
        return_bool: bool = False
    ) -> bool | Exception:
        """Nepovinná doplňková validace."""
        return True


    # ===================================
    # VNĚJŠÍ ROZHRANÍ KOMPOZITNÍ TŘÍDY
    # (metody jsou přidány při zpracování metadat)
    # ===================================

    @classmethod
    def calculate_value(
        cls: LogicSignature[P, R],
        *args: P.args,
        **kwargs: P.kwargs
    ) -> R:
        """
        Dynamicky spočítá hodnotu kompozice.
        Díky ParamSpec PyCharm nahlédne do uživatelské metody '_logic'
        a začne vývojáři našeptávat JEJÍ konkrétní parametry!
        """
        return calculate_value(cls, *args, *kwargs)

    @classmethod
    def decompose_value(
        cls: "SimpleObjectProtocol",
        value: Any
    ) -> Any:
        """Rozloží hlavní hodnotu na vnitřní komponenty."""
        return decompose_value(cls, value)

