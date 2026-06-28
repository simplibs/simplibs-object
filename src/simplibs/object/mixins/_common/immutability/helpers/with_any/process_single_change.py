from typing import Any, TYPE_CHECKING
from ...with_constant import with_constant
from ...with_composite import with_composite
# Annotations
if TYPE_CHECKING:
    from ......protocols.mixins.core_mixins import (
        InfrastructureProtocol,
        InfrastructuredComponent
    )
    from ......protocols.alias_typings import ChangeTuple


def process_single_change(
    self: "InfrastructureProtocol",
    change: "ChangeTuple"
) -> "InfrastructuredComponent":
    """
    Zpracuje jedinou změnu (name, value).
    Vrací novou instanci po aplikaci změny.

    !!! POŽADAVEK NA INTEGRACI !!!
    Tato funkce je navržena pro core pipeline frameworku. Objekt předaný v argumentu
    'instance' MUSÍ dědit z následujících mixinů (nebo implementovat jejich protokoly):
      1. Snapshot (poskytuje metodu _restore_snapshot)
      2. NodesDicts (poskytuje metadata a přístup k uzlům)
    Bez těchto předků pipeline vyhodí AttributeError.
    """

    # Validace struktury
    if (not isinstance(change, tuple)
        or len(change) != 2
        or not isinstance(change[0], str)):
        raise ...

    name, value = change

    # Konstanta
    if name in self._constant_names_tuple:
        return with_constant(self, name, value)

    # Kompozice
    if name in self.meta.node_names_set:
        return with_composite(self, name, value)

    # Neznámý název
    raise ...
