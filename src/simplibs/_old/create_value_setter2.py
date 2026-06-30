
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

    # 1. Vytvoření setteru pro root value
    if path is None:

        def setter(self: "SimpleInstanceLike", value: Any) -> None:

            # 1.2.1 Ověření zda hodnota není zamčená
            if self._locked:
                raise ValueError(f"{self.__class__.__name__} is locked.")

            # 2.2.2 Ověření zda objekt umožňuje dekompozice
            if not is_constant and not meta.is_decomposeable:
                raise_class_not_decomposeable(meta)

            # 1.2.3 Zápis hodnoty
            self._root_value_setter(value, recalculate_up=True)

            # 1.2.4 Přepočet hodnoty do inners
            if not is_constant:
                self._recalculate_inners()

            # 1.2.5 Případné logování
            self._log_outcome(value)

    # 2. Vytvoření setteru pro inners
    else:

        # 2.1 Definice metody pro přístup k instanci
        get_inner_instance = attrgetter(*path)

        def setter(self: "SimpleInstanceLike", value: Any) -> None:

            # 1.2.1 Ověření zda hodnota není zamčená
            if self._locked:
                raise ValueError(f"{self.__class__.__name__} is locked.")

            # 2.2.1 Získání instance
            inner_instance: "SimpleInstanceLike" = get_inner_instance(self)

            # 2.2.2 Ověření zda objekt umožňuje dekompozice
            if not is_constant and not meta.is_decomposeable:
                raise_class_not_decomposeable(meta)

            # 1.2.3 Zápis hodnoty
            # noinspection PyProtectedMember
            inner_instance._root_value_setter(value, recalculate_up=True)

            # 1.2.4 Přepočet hodnoty do inners
            if not is_constant:
                # noinspection PyProtectedMember
                inner_instance._recalculate_inners()

    # 3.  Přidání anotace
    setter.__annotations__ = {"value": meta.value_type, "return": None}

    # 4. Navrácení setteru
    return setter