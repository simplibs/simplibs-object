from typing import Any, TYPE_CHECKING
# Outers
from ..validations import process_value
# Inners
from .validations import verify_up_limit, verify_down_limit
# Annotations
if TYPE_CHECKING:
    from .....protocols.mixins.numerical.stepper import StepperProtocol


def set_value(
    self: "StepperProtocol",
    value: Any,
    *,
    validate: bool = True,
    raise_exception: bool = False
) -> Any:
    """
    Bezpečně zapíše novou hodnotu do instance s plnou kontrolou všech limitů a akcí.
    """
    # 1 Validace a nromalizace hodntoy
    _value = process_value(self, value, validate=validate)

    # 2. Vyřízení pro stejnou hodnotu
    # noinspection PyProtectedMember
    if _value == self._instance._value:
        return True

    # 3. Kontrola limitů
    # noinspection PyProtectedMember
    if _value > self._instance._value:
        if not verify_up_limit(self, _value, raise_exception=raise_exception):
            return False
    else:
        if not verify_down_limit(self, _value, raise_exception=raise_exception):
            return False

    # 4. Zápis hodnoty
    self._instance._value = _value
    return True