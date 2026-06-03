from typing import Any
from simplibs.sentinels import UNSET
# Inners
from ._metadata import SimpleMeta
from ._types import SimpleMetaType
from .settings import SimpleSettings


class SimpleBase(metaclass=SimpleMeta):
    """
    Abstraktní kořenová třída pro všechny prvky systému Simple.

    Tato třída definuje společnou identitu pro konstanty i kompozitní objekty.
    Zajišťuje napojení na metatřídu a poskytuje jednotné rozhraní pro 
    přístup k metadatům.
    """

    # ===================================
    # ZÁKLADNÍ ROZHRANÍ A NAPOJENÍ METADAT
    # (rozhraní společné všem potomkům)
    # ===================================

    #--- Definice __slots__ pro lepší výkon ---#
    # (každý potomek musí slots definovat jinak příjde o tuto výhodu)
    __slots__ = ()

    #--- Definice slotu pro metadata ---#
    # (pro základní třídy nastavuje hodnotu UNSET - vypočítává se pouze pro definiční třídy)
    __metadata__: SimpleMetaType = UNSET


    # ===================================
    # VNITŘNÍ ROZHRANÍ ZÁKLANÍ TŘÍDY
    # (definuje uživatel zakládající třídu)
    # ===================================

    #--- Hook pro případný loger ---#
    # (obsažen na konci každé vnější metody s přístupem k jejímu výsledku)
    @classmethod
    def _log_outcome(cls, outcome: Any) -> None:
        """
        Třídní hook pro případný loger výsledků metod.
        Volá se z třídních metod (validate, normalize atd.).
        """
        if SimpleSettings.logger:
            SimpleSettings.logger(cls, outcome)
