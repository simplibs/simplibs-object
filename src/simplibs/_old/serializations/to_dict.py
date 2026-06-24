# simplibs/serialization.py

def to_dict(obj):

    # 1. Vyřízení pro knstantu
    if obj.meta.is_constant:
        return obj.value

    # 2. Vyřízení pro kompozici
    return {
        inner.meta.name_snake: to_dict(inner)
        for inner in obj.meta.inners
    }

def to_dict2(obj):

    # 1. Vyřízení pro knstantu
    if obj.meta.is_constant:
        return {"value": obj.value}

    # 2. Vyřízení pro kompozici
    value = {"value": obj.value}
    return value.update({
        inner.meta.name_snake: getattr(obj, inner.meta.name_snake)
        for inner in obj.meta.inners
    })
