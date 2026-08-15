from typing import Any, NoReturn, TYPE_CHECKING
# Outers
from ....exceptions import SimpleObjectError
# Inners
from .validations import raise_unexpected_validation_error, raise_validation_error
# Annotations
if TYPE_CHECKING:
    from ...protocols.classes import SimpleConstantProtocol


def validate(
    cls: "SimpleConstantProtocol",
    value: Any,
    *,
    return_bool: bool = False,
) -> bool | None | NoReturn:
    """Runs the full validation pipeline: type validation + user-defined validation."""

    # 1. Run type validation and user-defined validation
    try:
        result = (
            cls.validate_type(value, return_bool=return_bool)
            and cls.meta.validate(value, return_bool=return_bool)
        )

    # 2. Handle exceptions raised during validation
    except Exception as e:

        # 2.1 Boolean mode — suppress errors and return False
        if return_bool:
            return False

        # 2.2 Expected SimpleObjectError — re-raise unchanged
        if isinstance(e, SimpleObjectError):
            raise

        # 2.3 Unexpected exception — wrap into a standardized error
        raise_unexpected_validation_error(cls, value, e)

    # 3. If validation returned False and we are not in boolean mode, raise error
    if result is False and not return_bool:
        raise_validation_error(cls, value)

    # 4. Return boolean result
    return result


_DESIGN_NOTES = """
# validate

## Purpose
Executes the complete validation pipeline for constant definitions. This pipeline
combines deterministic type validation with optional user-defined validation
logic (`_validate`). It ensures consistent behavior across all constant classes,
whether or not the user provides custom validation.

---

## Pipeline Structure
1. **Type Validation**
   - Performed via `cls.validate_type`.
   - Ensures the value matches the type declared in metadata.

2. **User-Defined Validation**
   - Performed via `cls.meta.validate`, which delegates to the class’s `_validate`
     method.
   - If the user does not override `_validate`, the default implementation
     returns `True`, meaning “no additional validation”.

---

## Exception Handling
- **Boolean Mode (`return_bool=True`)**
  - All errors are suppressed.
  - The function returns `False` for any failure.

- **Expected Errors (`SimpleObjectError`)**
  - Re-raised unchanged.
  - These represent structured, user-facing validation errors.

- **Unexpected Errors**
  - Wrapped using `raise_unexpected_validation_error`.
  - Ensures consistent error formatting even when user-defined validation
    raises arbitrary exceptions.

- **Validation Result = False**
  - Triggers `raise_validation_error`, indicating that validation failed without
    raising an exception.

---

## Notes
- This function is intentionally minimal; all diagnostic detail is delegated to
  the specialized error helpers.
- The default `_validate` method always returns `True`, allowing constants to
  rely solely on type validation unless the user explicitly adds custom logic.
- The public-facing docstring belongs to the class method `SimpleConstant.validate`,
  not to this internal helper.
"""