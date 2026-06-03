
def from_dict(cls, data):
    kwargs = {}
    for name, value in data.items():
        inner = cls.meta.inners_map[name]
        if inner.meta.is_constant:
            kwargs[name] = inner.meta.value_type(value)
        else:
            kwargs[name] = from_dict(inner, value)
    return cls(**kwargs)
