
from typing import Any, TYPE_CHECKING
from collections.abc import Callable
from operator import attrgetter
from .validations import raise_class_not_decomposeable
if TYPE_CHECKING:
    from .....protocols.metadata import SimpleMetadataLike
    from .....protocols.instance import SimpleInstanceLike
    from .....protocols.alias_typings import PathTuple


def create_value_setter(
    meta: "SimpleMetadataLike",
    is_constant: bool = False,
    path: PathTuple | None = None
) -> Callable:
    """
    Vytvoří setter funkci pro root nebo inner property.

    - is_composite=False → atomický setter (normalizace + kaskáda nahoru)
    - is_composite=True  → kompozitní setter (dekompozice + distribuce do inners)
    """

    # 1. Připrav attrgetter jednou — ne uvnitř setteru
    get_inner = attrgetter(*path) if path else None

    # 2. Vytvoření setteru pro root value
    def setter(self: "SimpleInstanceLike", value: Any) -> None:

        # 2.1 Ověření zda hodnota není zamčená
        if self._locked:
            raise ValueError(f"{self.__class__.__name__} is locked.")

        # 2.2 Ověření zda objekt umožňuje dekompozice (pouze u kompozic)
        if not is_constant and not meta.is_decomposeable:
            raise_class_not_decomposeable(meta)

        # 2.3 Získání instance
        instance = get_inner(self) if get_inner else self

        # 2.4 Zápis hodnoty (s přepočtem nahoru)
        # noinspection PyProtectedMember
        instance._root_value_setter(value, recalculate_up=True)

        # 2.5 Přepočet hodnoty do inners (pouze pro kompozice)
        if not is_constant:
            # noinspection PyProtectedMember
            instance._recalculate_inners()

        # 2.6 Logování (pouze pro hlavní hodnotu)
        if not path:
            from simplibs.object.settings.logging import log_value_event
            log_value_event(self.__class__, value, event="set")

    # 3.  Přidání anotace
    setter.__annotations__ = {"value": meta.value_type, "return": None}

    # 4. Navrácení setteru
    return setter