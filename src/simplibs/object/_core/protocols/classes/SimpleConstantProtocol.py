from typing import Protocol, Any, runtime_checkable, TYPE_CHECKING
# Inners
from .SimpleBaseProtocol import SimpleBaseProtocol
# Annotations
if TYPE_CHECKING:
    from ..alias_typings import ValidTypes


@runtime_checkable
class SimpleConstantProtocol(
    SimpleBaseProtocol,
    Protocol
):
    """
    Protocol for SimpleConstant. Represents the interface for constant classes (Atoms),
    including user-defined protected attributes and public validation methods.
    """

    # --- INTERNAL INTERFACE (Defined by the user when creating the class) ---
    _type: "ValidTypes"
    _default: Any

    @classmethod
    def _validate(cls, value: Any, *, return_bool: bool = False) -> bool | Exception:
        """Optional custom validation method defined by the user."""
        ...

    # --- EXTERNAL INTERFACE (Methods added/available for working with the constant) ---
    @classmethod
    def validate_type(cls, value: Any, *, return_bool: bool = False) -> bool:
        """Performs deterministic type validation based on class metadata."""
        ...

    @classmethod
    def validate(cls, value: Any, *, return_bool: bool = False) -> bool:
        """Performs type validation followed by custom method validation."""
        ...

    @classmethod
    def is_valid(cls, value: Any) -> bool:
        """Returns True if value passes complete validation, otherwise False."""
        ...

    @classmethod
    def normalize(cls, value: Any, *, process_none: bool = False) -> Any:
        """Normalizes value. Returns normalized value or raises SimpleRuntimeError."""
        ...

    @classmethod
    def bool_or_raise_validate_error(
        cls, value: Any, problem: str, *, return_bool: bool = False
    ) -> bool:
        """Helper method intended for use inside custom user '_validate' methods."""
        ...