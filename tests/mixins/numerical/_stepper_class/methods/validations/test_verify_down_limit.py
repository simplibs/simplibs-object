from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Annotations
if TYPE_CHECKING:
    from ......protocols.mixins.numerical.stepper import StepperProtocol


def verify_down_limit(
    self: "StepperProtocol",
    new_value: Any,
    *,
    raise_exception: bool = False
) -> bool:
    """
    Ověří, zda nová hodnota nepřekračuje spodní limit stepperu.

    Pokud je spodní limit nastaven a nová hodnota ho podkračuje,
    spustí případnou akci a volitelně vyvolá výjimku.
    """

    # 1. Kontrola zda je DOWN limit nastaven
    if self.down_limit is not UNSET and new_value < self.down_limit:

        # 2. Kontrola zda je nastavena akce
        if self.down_limit_action:
            self.down_limit_action()

        # 3. Kontrola zda se má vyvolat výjimka
        if raise_exception:
            raise ValueError("Dosaženo spodního limitu")
        return False

    # 4. Potvrzení úspěšné validace
    return True