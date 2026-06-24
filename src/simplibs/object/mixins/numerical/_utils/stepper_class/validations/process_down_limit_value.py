# Inners
from .process_value import process_value


def process_down_limit_value(self, value):

    # 1. Příprava hodnoty
    _value = process_value(self, value)

    # 2. Validace
    if self.up_limit < _value:
        raise "Down limit nemůže být vyší než up limit"
    return _value
