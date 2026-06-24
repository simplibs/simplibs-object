# Outers
from ..validations import process_value, verify_up_limit, verify_down_limit


# noinspection PyProtectedMember
def do_set_value(self, value, *, validate=True, raise_exception=False):
    """Zapíše hodnotu - kontroluje limity"""

    # 1 Validace a nromalizace hodntoy
    _value = process_value(self, value, validate=validate)

    # 2. Vyřízení pro stejnou hodnotu
    if _value == self._instance._value:
        return True

    # 3. Kontrola limitů
    if _value > self._instance._value:
        if not verify_up_limit(self, _value, raise_exception=raise_exception):
            return False
    else:
        if not verify_down_limit(self, _value, raise_exception=raise_exception):
            return False

    # 4. Zápis hodnoty
    self._instance._value = _value
    return True