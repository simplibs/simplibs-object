def process_value(self, value, *, validate=True):

    # 1. Normalizace hodnoty
    _value = (
        value if isinstance(value, self._value_type)
        else self._value_type(value)
    )

    # 2. Validace hodnoty
    if validate:
        self._instance.validate(_value)

    # 3. Navrácení hodnoty
    return _value
