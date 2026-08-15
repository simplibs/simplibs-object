from typing import Protocol, runtime_checkable, Any, Self, TYPE_CHECKING
# outers
from ..core_mixins import InfrastructureProtocol
# Annotations
if TYPE_CHECKING:
    from ...alias_typings import ChangesTuple, ChangesDict


@runtime_checkable
class ImmutableMethodsProtocol(
    InfrastructureProtocol,
    Protocol
):
    """
    Protocol for the ImmutableMethods mixin.

    Guarantees a complete set of methods for immutable (functional) state transformations.
    None of the methods mutate the existing instance; instead, they safely produce
    a new updated instance (Self).
    """

    # --- IMMUTABLE API - CORE ---

    def with_constants(
        self,
        changes_tuple: "ChangesTuple | None" = None
    ) -> Self:
        """
        Creates and returns a new immutable instance based on one or more
        provided changes to constant elements.
        """
        ...

    def with_constant(self, name: str, new_value: Any) -> Self:
        """
        Creates and returns a new immutable instance with an updated value
        for a single specific constant (atom) specified by its name.
        """
        ...

    def with_composite(self, name: str, new_value: Any) -> Self:
        """
        Creates and returns a new immutable instance with an updated value
        for a single specific composite element specified by its name.
        """
        ...

    # --- IMMUTABLE API - EXTENDED ---

    def with_changes(self, changes_dict: "ChangesDict") -> Self:
        """
        Ergonomic method allowing multiple constant change mappings to be provided
        as a standard dictionary. Returns a new immutable instance.
        """
        ...

    def with_value(self, new_value: Any) -> Self:
        """
        Ergonomic alias for updating the main value of this entire instance.
        Returns a new immutable instance.
        """
        ...

    def duplicate(self) -> Self:
        """
        Creates and returns an identical new copy (duplicate) of this immutable instance
        while preserving its full current state.
        """
        ...