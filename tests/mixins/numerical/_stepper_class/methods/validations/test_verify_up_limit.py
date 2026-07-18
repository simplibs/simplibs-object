from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Annotations
if TYPE_CHECKING:
    from ......protocols.mixins.numerical.stepper import StepperProtocol


def verify_up_limit(
    self: "StepperProtocol",
    new_value: Any,
    *,
    raise_exception: bool = False
) -> bool:
    """
    Ověří, zda nová hodnota nepřekračuje horní limit stepperu.

    Pokud je horní limit nastaven a nová hodnota ho překračuje,
    spustí případnou akci a volitelně vyvolá výjimku.
    """

    # 1. Kontrola zda je UP limit nastaven
    if self.up_limit is not UNSET and new_value > self.up_limit:

        # 2. Kontrola zda je nastavena akce
        if self.up_limit_action:
            self.up_limit_action()

        # 3. Kontrola zda se má vyvolat výjimka
        if raise_exception:
            raise ValueError("Dosaženo horního limitu")
        return False

    # 4. Potvrzení úspěšné validace
    return True