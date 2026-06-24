
# noinspection PyProtectedMember
def create_new_instance(instance, snapshot):
    # Vytvoření nové instance
    new_instance = object.__new__(type(instance))
    new_instance.__init__()

    # Načtení snapshotu
    new_instance._restore_snapshot(snapshot)

    # Navrácení instance
    return new_instance