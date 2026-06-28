from typing import Protocol, runtime_checkable, Any, Self
# Outers
from ...core_mixins import InfrastructureProtocol


@runtime_checkable
class CallProtocol(
    InfrastructureProtocol,
    Protocol
):
    """
    Protokol pro mixin Call.

    Garantuje schopnost volat instanci jako funkci (obj(...)) pro účely 
    hromadného zadávání změn a transformací vnitřního stavu. Vrací modifikovanou 
    verzi téhož typu (Self).
    """

    def __call__(self, *changes: Any, **kwargs: Any) -> Self:
        """
        Umožňuje volat instanci jako funkci a aplikovat na ni změny.

        Podporuje jak poziční argumenty (tuples, variace n-tic), 
        tak klíčové argumenty (kwargs). Veškerou logiku deleguje na engine with_any.
        """
        ...