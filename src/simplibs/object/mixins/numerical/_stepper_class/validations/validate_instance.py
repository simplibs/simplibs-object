from typing import TYPE_CHECKING
from numbers import Number
# Outers
from .....protocols.instance import SimpleInstanceType
# Annotations
if TYPE_CHECKING:
    from .....protocols.instance import SimpleInstanceLike


def validate_instance(
    instance: "SimpleInstanceLike"
) -> None:
    """
    Ověří, že předaná instance je validní pro použití ve stepperu.

    Kontroluje že instance splňuje minimální rozhraní SimpleInstanceType
    a že její hodnota podporuje numerické operace.
    """

    # 1. Validace instance vůči protokolu
    if not isinstance(instance, SimpleInstanceType):
        raise TypeError("Předaný objekt není validní instancí Simple systému")

    # 2. Validace že hodnota instance je numerická
    if not isinstance(instance.value, Number):
        raise TypeError(
            f"Hodnota instance musí být číselného typu, "
            f"obdrženo: {type(instance.value).__name__!r}"
        )