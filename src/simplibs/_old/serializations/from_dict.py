from .validations import raise_not_valid_operation


def from_dict(cls, data):

    # 1. Validace zda je možné použít funkci
    if not cls.meta.is_constant or not cls.meta.is_decomposeable:
        raise_not_valid_operation(cls, data)

    # 2. Vytvoření nové instance
    instance = cls()

    # 3. Vyřízení pro konstantu
    if cls.meta.is_constant:
        instance.value = data

    # 4. Vyřízení pro kompozici
    else:
        instance.value = cls.calculate_value(**data)

    # 5. Navrácení pozměnění instance (bez mixinů)
    return instance

def from_dict2(cls, data):

    # 1. Validace zda je možné použít funkci
    if not cls.meta.is_constant or not cls.meta.is_decomposeable:
        raise_not_valid_operation(cls, data)

    # 2. Vytvoření nové instance
    instance = cls()

    # 3. Zápis nové hodnoty
    instance.value = data["value"]

    # 4. Navrácení pozměnění instance (bez mixinů)
    return instance
