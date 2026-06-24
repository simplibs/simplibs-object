def process_limit_action(self, value):

    # 1. Validace
    if not callable(value):
        raise "Akce musí být volatelný objekt"

    # 2. Navrácení hodnoty
    return value