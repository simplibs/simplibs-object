from typing import Any
# Outers
from .......protocols import SimpleInstanceType
# Inners
from .helpers import (
    find_longest_keys,
    create_snapshot_dict,
    create_new_instance,
    reacalculate_owner_value
)


def with_constants(
    self: SimpleInstanceType,
    changes: tuple[str, Any] | tuple[tuple[str, Any], ...] = None
) -> SimpleInstanceType:

    # Vytvoření aktuálního snapshotu
    snapshot_dict = create_snapshot_dict(self._nodes_tuple)

    # Vytvoření slovníku pro cesty
    path_dict = {}

    # Vytvoření snapshotu
    new_snapshot = self._build_snapshot()

    # Přepsání snapshotu pokud je požadavek na změnu
    if changes:

        # Kontzrola zda bylo předané tuple
        if not isinstance(changes, tuple):
            raise ...

        # Pokud uvnitř tuple není další tuple - sjednocení vstupu
        if not isinstance(changes[0], tuple):
            changes = (changes,)

        # Procházení jednotlivých vniřních tuple
        for inner_tuple in changes:

            # Validace základní konstrukce vnitřního tuple
            if not isinstance(inner_tuple, tuple) or len(inner_tuple) != 2 or not isinstance(inner_tuple[0], str):
                raise ...

            # Vytvoření proměnných
            inner_name, new_value = inner_tuple

            # Validace zadaného prvku že je konstantou
            if not inner_name in self._constant_names:
                raise ...

            # Validace zadané hodnoty
            instance, path = self._nodes_dict[inner_name]
            instance.validate(new_value)

            # Zápis do slovníku snapshotu
            snapshot_dict[inner_name] = new_value

            # Zápis cesty
            path_dict[inner_name] = path

        # Vytažení klíčů nejdelších cest
        longest_key = find_longest_keys(path_dict)

        # Přepočet od nejdelších uzlů
        for key in longest_key:
            reacalculate_owner_value(snapshot_dict, key)

        # Vytvoření čistého snapshotu
        new_snapshot = tuple(snapshot_dict.values())
        # nebo:
        # new_snapshot = tuple(
        #     snapshot_dict[name]
        #     for name in self._node_names_set_tuple
        # )

    # Navrácení instance
    return create_new_instance(self, new_snapshot)