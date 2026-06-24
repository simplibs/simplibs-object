
# noinspection PyProtectedMember
def create_new_instance(
    instance,
    snapshot,
):
    """
    Co dělá:
        vytvoří novou instanci přes object.__new__(type(instance))
        zavolá __init__()
        zavolá _restore_snapshot(snapshot)
    """
    # Vytvoření nové instance
    new_instance = object.__new__(type(instance))
    new_instance.__init__()

    # Inicializace pro mutable objekty
    if new_instance.__is_mutable__:
        new_instance.init_mixins()

    # Načtení snapshotu
    new_instance._restore_snapshot(snapshot)

    # Navrácení instance
    return new_instance