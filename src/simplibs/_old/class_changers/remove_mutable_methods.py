def remove_mutable_methods(cls):
    for name in ("_root_value_setter", "_recalculate_self", "_recalculate_inners"):
        if hasattr(cls, name):
            delattr(cls, name)
