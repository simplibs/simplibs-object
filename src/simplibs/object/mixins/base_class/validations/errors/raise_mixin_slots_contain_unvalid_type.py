from typing import TYPE_CHECKING, NoReturn
# Outers
from .....exceptions import SimpleLogicError
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_slots_contain_unvalid_type(
    cls: "SimpleMixinProtocol",
) -> NoReturn:
    """
    Raises an error when '__slots__' contains items that are not strings.
    """

    slots = cls.__dict__["__slots__"]

    raise SimpleLogicError(
        error_name="MIXIN DEFINITION ERROR",
        label="__slots__",
        expected="All items inside __slots__ must be strings.",
        value=slots,
        problem=(
            f"Mixin '{cls.__name__}' defines '__slots__' with invalid items. ",
            "Every slot name must be of type 'str'."
        ),
        context=f"Mixin definition check: {cls.__name__}",
        how_to_fix=(
            "Ensure that all items inside __slots__ are strings.",
            "Example: __slots__ = ('flag', 'counter')",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_mixin_slots_contain_unvalid_type

## Purpose
Validates that every item inside the `__slots__` tuple is a string.  
Slot names must be simple identifiers, not objects, numbers, or other data types.

## Architectural reasoning
Mixins participate in dynamic class composition.  
To guarantee a predictable and conflict‑free memory layout:

- slot names must be strings,
- slot names must be statically analyzable,
- slot names must be safe to merge with other mixins and base classes.

If a mixin defines `__slots__` with non‑string items (e.g., integers, objects,
lists), Python cannot interpret them as valid slot identifiers. This would break:

- instance memory layout,
- attribute resolution,
- mixin merging logic,
- slot collision detection.

Therefore, strict enforcement of string-only slot names is required.

## Pipeline position
This function is called after verifying:

1. `__slots__` exists,
2. `__slots__` is tuple or string.

It is the third structural check in `verify_mixin_definition`.  
If any item is not a string → this error is raised immediately.

## Diagnostic value
The error message clearly identifies:

- the invalid slot structure,
- the mixin where the issue occurred,
- the expected format,
- actionable guidance for correction.

This makes debugging simple and prevents subtle runtime failures.

## Notes
- This is a pure `raise_...` function with no conditional logic.
- It is used exclusively by the mixin definition validator.
- All mixins must pass this check before they can be applied to instances.

"""