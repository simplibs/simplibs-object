from typing import TypeVar, ParamSpec, Protocol, Callable
# Outers
from ..type_chackings.SimpleMetaType import SimpleMetaType


# Typové proměnné pro magii s přenosem signatury
P = ParamSpec("P")
R = TypeVar("R")


class CopyLogicParams(Protocol[P, R]):
    """Protokol říkající: Jsem třída, která má metodu _logic s parametry P a návratem R."""
    @classmethod
    def _logic(cls, *args: P.args, **kwargs: P.kwargs) -> R: ...

    meta: SimpleMetaType
    _log_outcome: Callable