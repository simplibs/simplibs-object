from typing import TYPE_CHECKING, NoReturn
# Outers
from .....exceptions import SimpleLogicError
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_slots_unsuport_type(
    cls: "SimpleMixinProtocol",
) -> NoReturn:
    """
    Raises an error when '__slots__' is not of type tuple or str.
    """

    slots = cls.__dict__["__slots__"]

    raise SimpleLogicError(
        error_name="MIXIN DEFINITION ERROR",
        label="__slots__",
        expected="__slots__ must be a tuple or a string.",
        value=slots,
        problem=(
            f"Mixin '{cls.__name__}' defines '__slots__' using an invalid type: "
            f"{type(slots).__name__}."
        ),
        context=f"Mixin definition check: {cls.__name__}",
        how_to_fix=(
            "Use either a tuple or a string when defining __slots__.",
            "Example: __slots__ = ('a', 'b')",
            "Example: __slots__ = 'a'",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_mixin_slots_unsuport_type

## Purpose
Ensures that the `__slots__` attribute of a mixin is defined using one of the
two supported structural forms:

- a tuple of slot names, or  
- a single string representing one slot.

Any other container type (list, dict, set, custom object) is invalid and cannot
be used in the dynamic class‑composition pipeline.

## Architectural reasoning
Mixins participate in dynamic runtime class generation.  
To guarantee a predictable and conflict‑free memory layout:

- slot definitions must be simple,
- slot definitions must be immutable,
- slot definitions must be easily introspectable.

Python’s `__slots__` mechanism supports only strings and tuples of strings.
Allowing other types would break:

- slot validation,
- slot collision detection,
- instance memory layout consistency,
- mixin merging logic.

## Pipeline position
This function is called immediately after verifying that `__slots__` exists.
It is the second structural check in `verify_mixin_definition`:

1. `__slots__` must be present.  
2. `__slots__` must be tuple or string.  
3. If not → this error is raised and validation stops.

## Diagnostic value
The error message clearly identifies:

- the invalid type used,
- the mixin where the issue occurred,
- the expected structural form,
- actionable examples of correct usage.

This makes debugging straightforward and prevents subtle runtime failures.

## Notes
- This is a pure `raise_...` function with no conditional logic.
- It is used exclusively by the mixin definition validator.
- All mixins must pass this check before they can be applied to instances.
"""