from typing import Any, TYPE_CHECKING
# Outers
from ..core_mixins import Infrastructure
from .._commons.immutability import (
    with_constants,
    with_constant,
    with_composite,
    with_any,
    create_new_instance
)
# Inners
from ._validations import raise_with_changes_input_not_dict
# Annotations
if TYPE_CHECKING:
    from ..._core.protocols.mixins.immutable import ImmutableMethodsProtocol
    from ..._core.protocols.alias_typings import ChangesTuple, ChangesDict


class ImmutableMethods(Infrastructure):
    """
    Mixin poskytující immutable API pro práci s instancemi:

    - with_constants(...)
    - with_constant(...)
    - with_composite(...)

    Konstrukce immutable tříd (getter-only value, odstranění setterů,
    odstranění mutačních metod, immutable inners) je nyní řešena
    přímo v make_atom_class / make_composite_class.
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice určení
    _immutable_only = True

    # Definice slotů
    __slots__ = ()

    # ----------------------------------------
    # Methods - Immutable API (core)
    # ----------------------------------------

    def with_constants(
        self: "ImmutableMethodsProtocol",
        changes_tuple: "ChangesTuple | None" = None
    ) -> "ImmutableMethodsProtocol":
        """Vytvoří novou immutable instanci na základě více změn."""
        return with_constants(self, changes_tuple)

    def with_constant(
        self: "ImmutableMethodsProtocol",
        name: str,
        new_value: Any
    ) -> "ImmutableMethodsProtocol":
        """Vytvoří novou immutable instanci změnou jedné konstanty."""
        return with_constant(self, name, new_value)

    def with_composite(
        self: "ImmutableMethodsProtocol",
        name: str,
        new_value: Any
    ) -> "ImmutableMethodsProtocol":
        """Vytvoří novou immutable instanci změnou jedné kompozice."""
        return with_composite(self, name, new_value)

    # ----------------------------------------
    # Methods - Immutable API (extended)
    # ----------------------------------------

    def with_changes(
        self: "ImmutableMethodsProtocol",
        changes_dict: "ChangesDict"
    ) -> "ImmutableMethodsProtocol":
        """Metoda umožnující zadat více změn pro konstanty jako slovník"""
        if not isinstance(changes_dict, dict):
            raise_with_changes_input_not_dict(self, changes_dict)
        return with_any(self, tuple(changes_dict.items()))

    def with_value(
        self: "ImmutableMethodsProtocol",
        new_value: Any
    ) -> "ImmutableMethodsProtocol":
        """Metoda pro změnu hlavní hodnoty - alias pro pohodlné použití"""
        return self.with_composite(self.meta.name_snake, new_value)

    def duplicate(
        self: "ImmutableMethodsProtocol"
    ) -> "ImmutableMethodsProtocol":
        """Metoda vracejí novu instanci se stejnými hodnotami"""
        return create_new_instance(self, self._build_snapshot())