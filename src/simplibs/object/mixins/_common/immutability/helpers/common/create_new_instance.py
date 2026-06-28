from typing import Any, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ......protocols.mixins.core_mixins import (
        InfrastructureProtocol,
        InfrastructuredComponent
    )
    from ......protocols.alias_typings import SnapshotTuple


def create_new_instance(
    instance: "InfrastructureProtocol",
    snapshot: "SnapshotTuple",
) -> "InfrastructuredComponent":
    """
    Co dělá:
        vytvoří novou instanci přes object.__new__(type(instance))
        zavolá __init__()
        zavolá _restore_snapshot(snapshot)

    !!! POŽADAVEK NA INTEGRACI !!!
    Tato funkce je navržena pro core pipeline frameworku. Objekt předaný v argumentu
    'instance' MUSÍ dědit z následujících mixinů (nebo implementovat jejich protokoly):
      1. Snapshot (poskytuje metodu _restore_snapshot)
      2. NodesDicts (poskytuje metadata a přístup k uzlům)
    Bez těchto předků pipeline vyhodí AttributeError.
    """

    # 1. Vytvoření nové instance
    new_instance = object.__new__(type(instance))
    new_instance.__init__()

    # 2. Načtení snapshotu
    # noinspection PyProtectedMember
    new_instance._restore_snapshot(snapshot)

    # 3. Navrácení instance
    return new_instance

