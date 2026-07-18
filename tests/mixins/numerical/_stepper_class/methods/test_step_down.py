from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from .validations import process_step_value, verify_down_limit
# Annotations
if TYPE_CHECKING:
    from .....protocols.mixins.numerical.stepper import StepperProtocol
    from .....protocols.mixins.numerical.stepper.internal_types import StepValue


def step_down(
    self: "StepperProtocol",
    value: "StepValue" = UNSET,
    *,
    validate: bool = True,
    raise_exception: bool = False
) -> Any:
    """
    Posune hodnotu navázané instance směrem dolů o definovaný krok (nebo zadanou hodnotu).
    Kontroluje nastavené limity a spouští případné akce.
    """

    # 1 Validace a nromalizace hodntoy
    _value = process_step_value(self, value, validate=validate)

    # 2. Výpočet nové hodnoty
    # noinspection PyProtectedMember
    new_value = self._instance._value - _value

    # 3. Kontrola limitu
    if not verify_down_limit(self, new_value, raise_exception=raise_exception):
        return False

    # 4. Zápis hodnoty
    self._instance._value = new_value
    return True