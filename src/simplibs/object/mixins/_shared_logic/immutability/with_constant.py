from typing import Any
# Outers
from .......protocols import SimpleInstanceType
# Inners
from .helpers.common import (
    create_snapshot_dict,
    reacalculate_owner_value,
    create_new_instance
)


def with_constant(
    self: SimpleInstanceType,
    name: str,
    new_value: Any,
) -> SimpleInstanceType:
    """
    !!! POŽADAVEK NA INTEGRACI !!!
    Tato funkce je navržena pro core pipeline frameworku. Objekt předaný v argumentu
    'instance' MUSÍ dědit z následujících mixinů (nebo implementovat jejich protokoly):
      1. Snapshot (poskytuje metodu _restore_snapshot)
      2. NodesDicts (poskytuje metadata a přístup k uzlům)
    Bez těchto předků pipeline vyhodí AttributeError.
    """

    # Validace
    if name not in self._constant_names:
        raise ...

    # Validace zadané hodnoty
    instance, path = self._nodes_dict[name]
    instance.validate(new_value)

    # Vytvoření aktuálního snapshotu
    snapshot_dict = create_snapshot_dict(self._nodes_tuple)

    # Zápis nové hodnoty
    snapshot_dict[name] = new_value

    # Přepočet hodnot kompozic
    reacalculate_owner_value(snapshot_dict, instance.owner)

    # Vytvoření čistého snapshotu
    new_snapshot = tuple(snapshot_dict.values())

    # Navrácení instance
    return create_new_instance(self, new_snapshot)