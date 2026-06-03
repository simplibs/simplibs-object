from typing import Any
from simplibs.sentinels import UNSET, UnsetType
# Inners
from .SimpleConstant import SimpleConstant
from ._mixins.composition.CreateValue import CreateValue
from ._mixins.composition.DecomposeValue import DecomposeValue
from ._mixins.composition.UpdateValue import UpdateValue



class SimpleObject(
    # Metody logiky
    CreateValue,            # create_value(cls, **kwargs) -> Any
    DecomposeValue,         # decompose_value(cls, value: Any) -> Dict[str, Any]
    UpdateValue,            # update_value(cls, value: Any, **kwargs) -> Any
    # Základní třída
    SimpleConstant,
):

    # ===================================
    # ZÁKLADNÍ ROZHRANÍ DEFINICE TŘÍDY
    # ===================================

    # Přebírá z SimpleConstant:
    # _type  # Typ - Vždy povinný
    # _default  # Defaultní hodnota - Povinný pokud nemáme inners
    # _validate # metoda pro validace - Nepoviná

    # Vnitřní prvky - Povinný atribut pro kompozici
    _inners: tuple | UnsetType = UNSET

    @classmethod
    def _logic(cls, *args, **kwargs) -> UnsetType:
        """Povinná pro kompozici, vrací default pro atomy."""
        return UNSET

    @classmethod
    def _decompose(cls, value: Any) -> UnsetType:
        """Nepovinná, vrací None, pokud rozklad není podporován."""
        return UNSET


    # zda se nedá to vytvořit dinamicky
    create_value = cls.meta.logic
    # jak tvořit signaturu?
    @classmethod
    def create_value(cls):...

    # kde mít logiku která bude vytvářet objekt?



