from typing import TypeVar, ParamSpec, Protocol, Callable, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ..metadata import SimpleObjectMetadataProtocol


# Typové proměnné pro magii s přenosem signatury
# (MUSÍ být napřímo v runtime)
P = ParamSpec("P")
R = TypeVar("R")


class LogicSignature(Protocol[P, R]):
    """
    Protokol říkající: Jsem třída, která má metodu _logic s parametry P a návratem R.
    Slouží jako typová kotva pro dekorátory a kalkulační metody přenášející signaturu.
    """

    @classmethod
    def _logic(cls, *args: P.args, **kwargs: P.kwargs) -> R:
        ...

    # Používáme uvozovky, protože import žije v TYPE_CHECKING bloku
    meta: "SimpleObjectMetadataProtocol"
    _log_outcome: Callable