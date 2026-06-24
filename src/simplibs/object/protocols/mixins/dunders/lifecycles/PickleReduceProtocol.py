from typing import Protocol, runtime_checkable, Any
# Inners
from .PickleStateProtocol import PickleStateProtocol


@runtime_checkable
class PickleReduceProtocol(
    PickleStateProtocol,
    Protocol
):
    """
    Protokol pro mixin PickleReduce.

    Garantuje integraci s nízkoúrovňovým protokolem pickle pomocí 
    metody __reduce__, která definuje tovární rekonstrukční plán objektu.
    """

    def __reduce__(self) -> tuple[type, tuple[()], dict[str, Any]]:
        """
        Nativní Python pickle protokol.

        Vrací trojici obsahující:
        1. Class objekt pro znovuvytvoření instance (self.__class__)
        2. Prázdnou n-tici pozičních argumentů pro konstruktor
        3. Slovník stavu získaný skrze __getstate__()
        """
        ...