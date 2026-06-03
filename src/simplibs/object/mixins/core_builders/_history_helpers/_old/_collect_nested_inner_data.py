# noinspection PyProtectedMember
def _collect_nested_inner_data(instance, snapshot, path):
    # procházení inners
    for inner in instance.meta.inners:

        # Vyřízení prvku
        inner_meta = inner.meta
        name_snake = inner_meta.name_snake
        name_private = inner_meta.name_private

        inner_instance = getattr(instance, name_private)
        new_path = path + (name_private,)

        snapshot[name_snake] = (new_path, inner_instance._value)

        # Vyřízení kompozic
        if not inner_meta.is_constant:
            _collect_nested_inner_data(inner_instance, snapshot, new_path)