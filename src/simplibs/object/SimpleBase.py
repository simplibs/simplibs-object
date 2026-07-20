from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from ._core_logic.metadata import SimpleMeta
# Annotations
if TYPE_CHECKING:
    from .protocols.classes import SimpleBaseProtocol
    from .protocols.metadata import SimpleMetadataLike


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
    __metadata__: "SimpleMetadataLike" = UNSET

