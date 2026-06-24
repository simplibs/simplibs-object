from typing import Protocol, runtime_checkable
# Outers
from ...base_class import SimpleMixinProtocol


@runtime_checkable
class ValueDisplayProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protokol pro mixin ValueDisplay (původní ValueDisplayRepr).

    Garantuje, že se objekt navenek reprezentuje jako surová hodnota, 
    kterou obaluje. Přepisuje technické zobrazení (__repr__) pro debugging 
    a uživatelské zobrazení (__str__) pro textové výstupy.
    """

    def __repr__(self) -> str:
        """
        Vrací technický řetězec pro vývojáře a logování 
        ve formátu: ClassName(value_repr).
        """
        ...

    def __str__(self) -> str:
        """
        Vrací čistou lidsky čitelnou hodnotu převedenou na řetězec.
        """
        ...