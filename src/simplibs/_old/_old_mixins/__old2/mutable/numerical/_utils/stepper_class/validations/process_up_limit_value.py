# Inners
from .process_value import process_value


def process_up_limit_value(self, value):

    # 1. Příprava hodnoty
    _value = process_value(self, value)

    # 2. Validace
    if self.down_limit > _value:
        raise "Up limit nemůže být menší než down limit"
    return _value