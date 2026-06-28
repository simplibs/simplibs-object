from typing import TypeVar, ParamSpec, Protocol
# Outers
from ..classes import SimpleObjectProtocol


# Typové proměnné pro magii s přenosem signatury
# (MUSÍ být napřímo v runtime)
P = ParamSpec("P")
R = TypeVar("R")


class LogicSignature(SimpleObjectProtocol, Protocol[P, R]):
    """
    Protokol říkající: Jsem třída, která má metodu _logic s parametry P a návratem R.
    Slouží jako typová kotva pro dekorátory a kalkulační metody přenášející signaturu.
    """

    @classmethod
    def _logic(cls, *args: P.args, **kwargs: P.kwargs) -> R:
        ...
