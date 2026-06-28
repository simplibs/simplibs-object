from typing import TYPE_CHECKING
# Outers
from ...constants import BASE_CLASS_NAMES
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def calculate_blueprint_path(
    cls: "SimpleClassLike"
) -> str:
    """
    Pomocná metoda, která projde MRO a sestaví řetězec MojeTrida(Rodic).
    Ignoruje systémové kořeny jako SimpleObject, SimpleBase atd.
    """

    # 1. Vnitřní impor na základní třídu
    from .....SimpleBase import SimpleBase

    # 2. Kontrola předků
    # Vezmeme všechny předky z MRO, kteří jsou potomky SimpleBase,
    # ale nejsou to ty samé systémové kořeny (SimpleObject, SimpleConstant, SimpleBase)
    parents = [
        mro_class.__name__ for mro_class in cls.__mro__
        if issubclass(mro_class, SimpleBase) and
           mro_class.__name__ not in BASE_CLASS_NAMES and
           mro_class != cls
    ]

    # 3. Vytvoření a navrácení řetězce
    return (
        cls.__name__
        if not parents else
        f"{cls.__name__}({', '.join(parents)})"
    )