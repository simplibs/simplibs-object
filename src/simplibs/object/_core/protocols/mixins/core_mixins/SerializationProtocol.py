from typing import Protocol, runtime_checkable, Any, Self, TYPE_CHECKING
# Inners
from .InfrastructureProtocol import InfrastructureProtocol
# Annotations
if TYPE_CHECKING:
    from ...alias_typings import StateDict


@runtime_checkable
class SerializationProtocol(
    InfrastructureProtocol,
    Protocol
):
    """
    Protocol for the universal master mixin Serialization.

    Guarantees a complete set of methods for export (to_dict, to_json) and
    import/update (from_dict, from_json, update_constants, update) of object data.
    Safely covers both in-place mutations and immutable transformations.
    """

    # ----------------------------------------
    # 1) EXPORT (Export API)
    # ----------------------------------------
    def to_dict(self, *, constant_only: bool = False) -> "StateDict":
        """Serializes the instance into a human-readable flat dictionary."""
        ...

    def to_json(self, **kwargs: Any) -> str:
        """Serializes the instance into a JSON formatted string."""
        ...

    # ----------------------------------------
    # 2) IMPORT / UPDATE (Import API supporting Fluent API)
    # ----------------------------------------
    def from_dict(self, user_dict: "StateDict") -> Self:
        """
        Reconstructs the instance state from the provided dictionary.
        Returns the instance (Self) to enable method chaining.
        """
        ...

    def from_json(self, json_str: str) -> Self:
        """
        Reconstructs the instance state from a JSON string.
        Returns the instance (Self) to enable method chaining.
        """
        ...

    def update_constants(self, user_dict: "StateDict") -> Self:
        """
        Updates constants (atoms) from the provided partial or full dictionary.
        Returns the instance (Self) to enable method chaining.
        """
        ...