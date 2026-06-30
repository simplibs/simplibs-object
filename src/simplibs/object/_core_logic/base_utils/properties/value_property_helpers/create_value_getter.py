
from typing import Any, TYPE_CHECKING
from collections.abc import Callable
from operator import attrgetter
if TYPE_CHECKING:
    from .....protocols.metadata import SimpleMetadataLike
    from .....protocols.instance import SimpleInstanceLike
    from .....protocols.alias_typings import PathTuple


def create_value_getter(
    meta: "SimpleMetadataLike",
    path: PathTuple | None
) -> Callable:
    """
    Vytvoří getter funkci pro root nebo inner property.

    Getter je stejný pro atomické i kompozitní property —
    v obou případech vrací self._value nebo inner_instance.value.
    """

    # 1. Vytvoření getteru pro root value
    if path is None:
        def getter(self: "SimpleInstanceLike") -> Any:
            return self._value

    # 2. Vytvoření getteru pro inners
    else:
        get_inner_instance = attrgetter(*path)
        def getter(self) -> Any:
            return get_inner_instance(self).value

    # 3. Přidání návratové anotace
    getter.__annotations__ = {"return": meta.value_type}

    # 4. Vrácení getteru
    return getter