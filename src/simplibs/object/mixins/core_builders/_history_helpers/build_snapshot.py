from ._collect_nested_inner_data import _collect_nested_inner_data

# noinspection PyProtectedMember
def build_snapshot(instance):
    """
    Vytvoří snapshot všech hodnot (_value) včetně všech inners.
    Vrací tuple:
        (name_snake,path_tuple, value)
    """

    # 1. Definice prázdné cesty
    path = ()

    # 2. Definice seznamu
    snapshot = [(path, instance._value),]

    # 3. Rekurzivní přidání vnitřních prvků
    if not instance.meta.is_constant:
        _collect_nested_inner_data(instance, path, snapshot)

    # 4. Navrácení tuple
    return tuple(snapshot)


