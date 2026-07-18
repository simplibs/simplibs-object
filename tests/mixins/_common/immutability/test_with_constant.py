from typing import Any, TYPE_CHECKING
# Inners
from .helpers.common import (
    create_snapshot_dict,
    reacalculate_owner_value,
    create_new_instance
)
# Annotations
if TYPE_CHECKING:
    from ....protocols.mixins.core_mixins import (
        InfrastructureProtocol,
        InfrastructuredComponent
    )


def with_constant(
    self: "InfrastructureProtocol",
    name: str,
    new_value: Any,
) -> "InfrastructuredComponent":
    """
    !!! POŽADAVEK NA INTEGRACI !!!
    Tato funkce je navržena pro core pipeline frameworku. Objekt předaný v argumentu
    'instance' MUSÍ dědit z následujících mixinů (nebo implementovat jejich protokoly):
      1. Snapshot (poskytuje metodu _restore_snapshot)
      2. NodesDicts (poskytuje metadata a přístup k uzlům)
    Bez těchto předků pipeline vyhodí AttributeError.
    """

    # 1. Validace
    if name not in self._constant_names_tuple:
        raise ...

    # 2. Validace zadané hodnoty
    instance, path = self._nodes_dict[name]
    instance.validate(new_value)

    # 3. Vytvoření aktuálního snapshotu
    snapshot_dict = create_snapshot_dict(self._nodes_tuple)

    # 4. Zápis nové hodnoty
    snapshot_dict[name] = new_value

    # 5. Přepočet hodnot kompozic
    reacalculate_owner_value(snapshot_dict, instance.owner)

    # 6. Vytvoření čistého snapshotu
    new_snapshot = tuple(snapshot_dict.values())

    # 7. Navrácení instance
    return create_new_instance(self, new_snapshot)