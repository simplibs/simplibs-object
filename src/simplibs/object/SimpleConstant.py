from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from .SimpleBase import SimpleBase
from ._core.logic.constant_methods import validate_type as _validate_type
from ._core.logic.constant_methods import validate as _validate
from ._core.logic.constant_methods import normalize as _normalize
from ._core.logic.constant_methods import bool_or_raise_validate_error as _bool_or_raise_validate_error
# Annotations
if TYPE_CHECKING:
    from ._core.protocols.classes import SimpleConstantProtocol
    from ._core.protocols.alias_typings import ValidTypes


class SimpleConstant(SimpleBase):
    """
    Declarative base class for defining constant nodes in the Simple system.

    A SimpleConstant represents a single typed value with:
    - a declared type,
    - a default value,
    - optional extended validation logic.

    Constants serve as the foundational building blocks for composite objects
    (`SimpleObject`). They can also be used independently in other libraries
    (e.g., validation frameworks) where typed, self-validating values are needed.
    """

    # ----------------------------------------------------------------------
    # 1) Declarative interface (user-defined)
    # ----------------------------------------------------------------------

    # Required type annotation for the constant's value.
    # Must be provided by the user and must pass type validation.
    _type: "ValidTypes" = UNSET

    # Default value for the constant.
    # Must be provided by the user and must pass type validation.
    _default: Any = UNSET

    @classmethod
    def _validate(
        cls,
        value: Any,
        *,
        return_bool: bool = False,
    ) -> bool | Exception:
        """
        Optional extended validation hook.

        Users may override this method to provide additional validation beyond
        basic type checking. The method may:

        - return True/False,
        - raise a custom exception,
        - or use `bool_or_raise_validate_error` for structured error reporting.

        If not overridden, the method defaults to accepting all values that
        pass type validation.
        """
        return True

    # ----------------------------------------------------------------------
    # 2) Public class-level API (deterministic, metadata-driven)
    # ----------------------------------------------------------------------

    @classmethod
    def validate_type(
        cls: "SimpleConstantProtocol",
        value: Any,
        *,
        return_bool: bool = False,
    ) -> bool | None:
        """Perform deterministic type validation based on class metadata.

        Args:
            value: The value to validate against the constant's declared type.
            return_bool: If True, return a boolean instead of raising errors.

        Returns:
            True if the value matches the declared type.
            False if `return_bool=True` and the value is invalid.
            None if `return_bool=False` and validation succeeds.

        Raises:
            SimpleRuntimeError: If `return_bool=False` and the value does not match the type.
        """
        return _validate_type(cls, value, return_bool=return_bool)

    @classmethod
    def validate(
        cls: "SimpleConstantProtocol",
        value: Any,
        *,
        return_bool: bool = False,
    ) -> bool | None:
        """Perform full validation of the value.

        Full validation includes:
        - deterministic type validation,
        - extended validation via `_validate`.

        Args:
            value: The value to validate.
            return_bool: If True, return a boolean instead of raising errors.

        Returns:
            True if the value passes full validation.
            False if `return_bool=True` and validation fails.
            None if `return_bool=False` and validation succeeds.

        Raises:
            SimpleRuntimeError: If `return_bool=False` and validation fails.
        """
        return _validate(cls, value, return_bool=return_bool)

    @classmethod
    def is_valid(
        cls: "SimpleConstantProtocol",
        value: Any,
    ) -> bool | None:
        """Check whether the value passes full validation.

        This is a convenience wrapper around `validate(..., return_bool=True)`.

        Args:
            value: The value to validate.

        Returns:
            True if the value is valid, otherwise False.
        """
        return cls.validate(value, return_bool=True)

    @classmethod
    def normalize(
        cls: "SimpleConstantProtocol",
        value: Any,
        *,
        process_none: bool = False,
    ) -> Any:
        """Normalize the value according to class metadata.

        Normalization may include:
        - default substitution,
        - type enforcement,
        - extended validation,
        - optional handling of None values.

        Args:
            value: The value to normalize.
            process_none: If True, None may be replaced by the default value.

        Returns:
            The normalized value.

        Raises:
            SimpleRuntimeError: If the value cannot be normalized or fails validation.
        """
        return _normalize(cls, value, process_none=process_none)

    @classmethod
    def bool_or_raise_validate_error(
        cls: "SimpleConstantProtocol",
        value: Any,
        problem: str,
        *,
        return_bool: bool = False,
    ) -> bool:
        """Helper for user-defined `_validate` methods.

        This method allows concise validation logic while still providing structured
        error reporting.

        Args:
            value: The value being validated.
            problem: Human-readable description of the validation failure.
            return_bool: If True, return False instead of raising an error.

        Returns:
            False if `return_bool=True`.

        Raises:
            SimpleRuntimeError: If `return_bool=False` and validation fails.
        """
        return _bool_or_raise_validate_error(cls, value, problem, return_bool=return_bool)


_DESIGN_NOTES = """
# SimpleConstant — Declarative Constant Node

## Purpose
`SimpleConstant` defines the declarative interface for constant nodes in the
Simple system. A constant represents a single typed value with:

- a required type annotation (`_type`),
- a required default value (`_default`),
- optional extended validation logic (`_validate`).

Constants are used both independently and as inner elements of composite objects
(`SimpleObject`). They form the atomic building blocks of the Simple ecosystem.

---

## 1. Declarative Interface

### `_type`
A required type annotation describing the value the constant represents.
This type is enforced at runtime through deterministic type validation.

### `_default`
A required default value. The default must pass type validation and serves as the
fallback value during normalization.

### `_validate`
An optional user-defined validation method. It allows developers to extend
validation beyond basic type checking. The method may:

- return `True` or `False`,
- raise a custom exception,
- or use `bool_or_raise_validate_error` for structured error reporting.

This hook is especially useful when type validation alone is insufficient.

---

## 2. Public Class-Level API

The following methods are automatically attached to every `SimpleConstant`
through metadata processing:

### `validate_type`
Performs deterministic type validation based solely on metadata.

### `validate`
Performs full validation:
- type validation,
- extended validation via `_validate`.

### `is_valid`
Convenience wrapper returning a boolean result.

### `normalize`
Normalizes values according to metadata rules:
- default substitution,
- type enforcement,
- structured error reporting.

### `bool_or_raise_validate_error`
A helper for writing clean, structured validation logic inside `_validate`.

---

## 3. Architectural Role

`SimpleConstant` is the foundation of the Simple system:

- It provides typed, self-validating values.
- It forms the inner elements of composite objects.
- It ensures deterministic behavior through metadata.
- It exposes a stable, public API for validation and normalization.

Composite objects (`SimpleObject`) inherit from `SimpleConstant`, extending the
model with inner elements and composite logic.

---

## Notes
- `SimpleConstant` is declarative; it defines structure, not behavior.
- All runtime behavior is delegated to metadata and core logic functions.
- Constants are immutable by design and serve as stable building blocks.
"""