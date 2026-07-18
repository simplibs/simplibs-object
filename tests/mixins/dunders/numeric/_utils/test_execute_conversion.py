from typing import TYPE_CHECKING, Any
from collections.abc import Callable
# Annotations
if TYPE_CHECKING:
    from .....protocols.mixins.dunders.numeric import ConversionProtocol


def execute_conversion(
    self: "ConversionProtocol",
    func: Callable[..., Any],
    *args: Any
) -> Any:
    """
    Rychlý modulární exekutor pro nativní konverze hodnoty.
    Provádí transformaci a formátuje unifikovanou chybovou hlášku při selhání.
    """

    # 1. Pokus o výpočet
    try:
        return func(self.value, *args)

    # 2. Vyvolání výjimky při neúspěchu
    except (TypeError, ValueError) as e:
        raise TypeError(
            f"Nelze provést {func.__name__}() na {self.meta.class_name} "
            f"(value={self.value!r}): {e}"
        ) from e
