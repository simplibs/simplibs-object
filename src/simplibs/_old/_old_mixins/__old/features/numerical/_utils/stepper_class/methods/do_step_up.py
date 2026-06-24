from simplibs.sentinels import UNSET
# Outers
from ..validations import process_step_value, verify_up_limit


# noinspection PyProtectedMember
def do_step_up(self, value=UNSET, *, validate=True, raise_exception=False):
    """Posune hodnotu nahoru"""

    # 1 Validace a nromalizace hodntoy
    _value = process_step_value(self, value, validate=validate)

    # 2. Výpočet nové hodnoty
    new_value = self._instance._value + _value

    # 3. Kontrola limitu
    if not verify_up_limit(self, new_value, raise_exception=raise_exception):
        return False

    # 4. Zápis hodnoty
    self._instance._value = new_value
    return True