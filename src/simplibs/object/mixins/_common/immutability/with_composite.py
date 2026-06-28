from typing import Any, TYPE_CHECKING
# Inners
from .with_constant import with_constant
from .helpers.with_composite import reacalculate_inners
from .helpers.common import (
    create_snapshot_dict,
    reacalculate_owner_value,
    create_new_instance,
)
# Annotations
if TYPE_CHECKING:
    from ....protocols.mixins.core_mixins import (
        InfrastructureProtocol,
        InfrastructuredComponent
    )


def with_composite(
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

    # 1. Kontrola zda nejde o konstantu
    if name in self._constant_names_tuple:
        return with_constant(self, name, new_value)

    # 2. Validace
    if name not in self.meta.node_names_set or not self.meta.is_decomposeable:
        raise ...

    # 3. Validace zadané hodnoty
    instance, path = self._nodes_dict[name]
    instance.validate(new_value)

    # 4. Vytvoření aktuálního snapshotu
    snapshot_dict = create_snapshot_dict(self._nodes_tuple)

    # 5. Zápis nové hodnoty
    snapshot_dict[name] = new_value

    # 6. Přepočet vnitřních prvků
    reacalculate_inners(snapshot_dict, instance.meta, new_value)

    # 7. Přepočet hodnot kompozic
    reacalculate_owner_value(snapshot_dict, instance.owner)

    # 8. Vytvoření čistého snapshotu
    new_snapshot = tuple(snapshot_dict.values())

    # 9. Navrácení instance
    return create_new_instance(self, new_snapshot)