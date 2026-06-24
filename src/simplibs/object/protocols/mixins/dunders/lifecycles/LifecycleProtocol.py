from typing import Protocol, runtime_checkable
# Inners
from .CopyableProtocol import CopyableProtocol
from .PickleReduceProtocol import PickleReduceProtocol


@runtime_checkable
class LifecycleProtocol(
    CopyableProtocol,
    PickleReduceProtocol,
    Protocol
):
    """
    Protokol pro master mixin Lifecycle.

    Zastřešuje kompletní životní cyklus instance v Pythonu. Plně kombinuje
    schopnost bezpečné replikace (mělké i hluboké kopírování) s nízkoúrovňovou
    podporou pro ukládání, obnovu a redukci stavu (pickle protokol).
    """

    # Samotný master mixin je pouze strukturální spojka, nemá žádné vlastní sloty ani metody.