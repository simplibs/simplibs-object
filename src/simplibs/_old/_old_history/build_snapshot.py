from ._collect_nested_inner_data import _collect_nested_inner_data

# noinspection PyProtectedMember
def build_snapshot(instance):
    """
    Vytvoří snapshot všech hodnot (_value) včetně všech inners.
    Vrací dict:
        name_snake: (path_tuple, value)
    """

    # Definice slovníku
    snapshot = {}

    # Zápis vlastní value
    name_snake = instance.meta.name_snake
    path = ()
    snapshot[name_snake] = (path, instance._value)

    # Zápis innerů
    if not instance.meta.is_constant:
        _collect_nested_inner_data(instance, snapshot, path)

    # Navrácení
    return snapshot


