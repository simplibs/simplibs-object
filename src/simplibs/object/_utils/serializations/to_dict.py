# simplibs/serialization.py

def to_dict(obj):
    if obj.is_atom:
        return obj.value

    result = {}
    for inner in obj.meta.inners:
        inner_obj = getattr(obj, inner.name_snake)
        result[inner.name_snake] = to_dict(inner_obj)
    return result

