# Outers
from ......protocols import SimpleInstanceType


def validate_instance(instance: SimpleInstanceType):

    # 1. Validace předků
    from ......SimpleObject import SimpleObject
    from ......SimpleConstant import SimpleConstant
    if not issubclass(instance, (SimpleConstant, SimpleObject)):
        raise "Nejedná se o validní instanci"

    # 2. Validace požadovaných úkonů
    instance: SimpleInstanceType
    value = instance.value
    try:
        _ = value + value
        _ = value - value
        _ = value == value
        _ = value < value
        _ = value > value
    except Exception as e:
        raise "Nepodporovaný typ"