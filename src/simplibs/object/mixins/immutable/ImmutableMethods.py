from typing import Any
# Outers
from ...protocols import SimpleInstanceType
from ..core_mixins import NodesDicts, Snapshot
from .._shared_logic.constants import VALUE
from .._shared_logic.immutability import (
    with_constants,
    with_constant,
    with_composite,
    with_any,
    create_new_instance
)



# noinspection PyProtectedMember
# noinspection PyAttributeOutsideInit
class ImmutableMethods(NodesDicts, Snapshot):
    """
    Mixin poskytující immutable API pro práci s instancemi:

    - with_constants(...)
    - with_constant(...)
    - with_composite(...)

    Konstrukce immutable tříd (getter-only value, odstranění setterů,
    odstranění mutačních metod, immutable inners) je nyní řešena
    přímo v make_atom_class / make_composite_class.
    """

    # Definice určení
    _immutable_only = True

    # Definice slotů
    __slots__ = ("_constant_names",)

    # Inicializace mixinu
    def init_mixins(self):
        super().init_mixins()

        # Seznam jmen konstant (tj. atomických prvků)
        self._constant_names = {
            instance.meta.name_snake
            for instance, path in self._nodes_tuple
            if path[-1] is not VALUE
        }

    # ---------------------------------------------------------
    # Immutable API - core
    # ---------------------------------------------------------

    def with_constants(
        self,
        changes_tuple: tuple[str, Any] | tuple[tuple[str, Any], ...] | None = None
    ) -> SimpleInstanceType:
        """Vytvoří novou immutable instanci na základě více změn."""
        return with_constants(self, changes_tuple)

    def with_constant(
        self,
        name: str,
        new_value: Any
    ) -> SimpleInstanceType:
        """Vytvoří novou immutable instanci změnou jedné konstanty."""
        return with_constant(self, name, new_value)

    def with_composite(
        self,
        name: str,
        new_value: Any
    ) -> SimpleInstanceType:
        """Vytvoří novou immutable instanci změnou jedné kompozice."""
        return with_composite(self, name, new_value)

    # ---------------------------------------------------------
    # Immutable API - extended
    # ---------------------------------------------------------

    def with_changes(self, changes_dict):
        """Metoda umožnující zadat více změn pro konstanty jako slovník"""
        if not isinstance(changes_dict, dict):
            raise ...
        return with_any(self, tuple(changes_dict.items()))

    def with_value(self, new_value: Any):
        """Metoda pro změnu hlavní hodnoty - alias pro pohodlné použití"""
        return self.with_composite(self.meta.name_snake, new_value)

    def duplicate(self):
        """Metoda vracejí novu instanci se stejnými hodnotami"""
        return create_new_instance(self, self._build_snapshot())