from typing import Any, TYPE_CHECKING
# Inners
from .helpers.with_constants import find_longest_keys
from .helpers.common import (
    create_snapshot_dict,
    create_new_instance,
    reacalculate_owner_value
)
# Annotations
if TYPE_CHECKING:
    from ....protocols.mixins.core_mixins import (
        InfrastructureProtocol,
        InfrastructuredComponent
    )
    from ....protocols.alias_typings import ChangeTuple, ChangesTuple


def with_constants(
    self: "InfrastructureProtocol",
    changes: "ChangeTuple | ChangesTuple | None" = None
) -> "InfrastructuredComponent":
    """
    !!! POŽADAVEK NA INTEGRACI !!!
    Tato funkce je navržena pro core pipeline frameworku. Objekt předaný v argumentu
    'instance' MUSÍ dědit z následujících mixinů (nebo implementovat jejich protokoly):
      1. Snapshot (poskytuje metodu _restore_snapshot)
      2. NodesDicts (poskytuje metadata a přístup k uzlům)
    Bez těchto předků pipeline vyhodí AttributeError.
    """

    # 1. Vytvoření aktuálního snapshotu
    snapshot_dict = create_snapshot_dict(self._nodes_tuple)

    # 2. Vytvoření slovníku pro cesty
    path_dict = {}

    # 3. Vytvoření snapshotu
    new_snapshot = self._build_snapshot()

    # 4. Přepsání snapshotu pokud je požadavek na změnu
    if changes:

        # 4.1 Kontzrola zda bylo předané tuple
        if not isinstance(changes, tuple):
            raise ...

        # 4.2 Pokud uvnitř tuple není další tuple - sjednocení vstupu
        if not isinstance(changes[0], tuple):
            changes = (changes,)

        # 4.3 Procházení jednotlivých vniřních tuple
        for inner_tuple in changes:

            # 4.3.1 Validace základní konstrukce vnitřního tuple
            if (not isinstance(inner_tuple, tuple)
                or len(inner_tuple) != 2
                or not isinstance(inner_tuple[0], str)):
                raise ...

            # 4.3.2 Vytvoření proměnných
            inner_name, new_value = inner_tuple

            # 4.3.3 Validace zadaného prvku že je konstantou
            if not inner_name in self._constant_names_tuple:
                raise ...

            # 4.3.4 Validace zadané hodnoty
            instance, path = self._nodes_dict[inner_name]
            instance.validate(new_value)

            # 4.3.5 Zápis do slovníku snapshotu
            snapshot_dict[inner_name] = new_value

            # 4.3.6 Zápis cesty
            path_dict[inner_name] = path

        # 4.4 Vytažení klíčů nejdelších cest
        longest_key = find_longest_keys(path_dict)

        # 4.5 Přepočet od nejdelších uzlů
        for key in longest_key:
            instance = self._nodes_instance_dict[key]
            reacalculate_owner_value(snapshot_dict, instance.owner)

        # 4.6 Vytvoření čistého snapshotu
        new_snapshot = tuple(snapshot_dict.values())

    # 5. Navrácení instance
    return create_new_instance(self, new_snapshot)