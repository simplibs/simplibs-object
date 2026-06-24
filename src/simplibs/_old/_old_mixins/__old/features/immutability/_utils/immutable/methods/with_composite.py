from typing import Any
# Outers
from .......protocols import SimpleInstanceType
# Inners
from .helpers import (
    create_snapshot_dict,
    reacalculate_owner_value,
    create_new_instance,
    reacalculate_inners
)


def with_composite(
    self: SimpleInstanceType,
    name: str,
    new_value: Any
) -> SimpleInstanceType:

    # Kontrola zda nejde o konstantu
    if name in self._constant_names:
        return self.with_constant(name, new_value)

    # Validace
    if name not in self.meta.node_names_set or not self.meta.is_decomposeable:
        raise ...

    # Validace zadané hodnoty
    instance, path = self._nodes_dict[name]
    instance.validate(new_value)

    # Vytvoření aktuálního snapshotu
    snapshot_dict = create_snapshot_dict(self._nodes_tuple)

    # Zápis nové hodnoty
    snapshot_dict[name] = new_value

    # Přepočet vnitřních prvků
    reacalculate_inners(snapshot_dict, instance.meta, new_value)

    # Přepočet hodnot kompozic
    reacalculate_owner_value(snapshot_dict, name)

    # Vytvoření čistého snapshotu
    new_snapshot = tuple(snapshot_dict.values())

    # Navrácení instance
    return create_new_instance(self, new_snapshot)