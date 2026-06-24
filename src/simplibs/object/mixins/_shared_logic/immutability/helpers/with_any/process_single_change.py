from typing import Any
from ...with_constant import with_constant
from ...with_composite import with_composite


def process_single_change(self, change: tuple[str, Any]):
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
    if name in self._constant_names:
        return with_constant(self, name, value)

    # Kompozice
    if name in self.meta.node_names_set:
        return with_composite(self, name, value)

    # Neznámý název
    raise ...
