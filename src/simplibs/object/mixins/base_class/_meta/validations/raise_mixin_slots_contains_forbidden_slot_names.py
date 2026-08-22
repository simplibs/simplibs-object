from typing import TYPE_CHECKING, NoReturn
# Outers
from ...._common_logic.constants import FORBIDDEN_NAMES
from .....exceptions import SimpleRuntimeError
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_slots_contains_forbidden_slot_names(
    cls: "SimpleMixinProtocol",
    slots_set: set[str],
) -> NoReturn:
    """
    Raises an error when '__slots__' contains names that collide with
    internal Simple system attributes.
    """

    forbidden_found = FORBIDDEN_NAMES & slots_set
    forbidden_list = tuple(sorted(forbidden_found))

    raise SimpleRuntimeError(
        error_name="MIXIN DEFINITION ERROR",
        label="Forbidden slot names in __slots__",
        expected="Mixin __slots__ must not contain names reserved by the Simple system.",
        value=forbidden_list,
        problem=(
            f"Mixin '{cls.__name__}' defines forbidden slot names inside '__slots__':",
            *[f"• {name}" for name in forbidden_list],
            "These names are reserved for internal Simple system mechanics.",
        ),
        context=f"Mixin definition check: {cls.__name__}",
        how_to_fix=(
            "Remove all forbidden names from the __slots__ definition.",
            "Use unique, non-conflicting slot identifiers.",
            "Recommended: prefix mixin slots with '_mx_' or '_mixin_'.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_mixin_slots_contains_forbidden_slot_names

## Purpose
Validates that the mixin does not declare forbidden names inside its `__slots__`.
Slot names represent instance-level attributes, and certain names are reserved
for internal Simple system mechanics. These reserved names must never appear
inside user-defined mixins.

## Architectural reasoning
The Simple system uses several internal attributes to manage:

- value storage (`_value`)
- ownership (`_owner`)
- composite structure (`_inners`)
- reactive recalculation (`_recalculate_self`, `_recalculate_inners`)
- metadata access (`meta`, `__metadata__`)
- logic evaluation (`_logic`)
- decomposition (`_decompose`)

If a mixin defines any of these names inside `__slots__`, it would:

- override internal runtime behavior,
- corrupt instance memory layout,
- break reactive recalculation,
- shadow core properties,
- cause unpredictable runtime failures.

Therefore, strict enforcement is required.

## Why this check is separate from forbidden class attributes
This validation checks **instance-level attributes** declared in `__slots__`.

A separate validation step checks **class-level attributes** declared in
`cls.__dict__`. These two checks serve different architectural layers and
must remain independent.

## Pipeline position
This check occurs after verifying:

1. `__slots__` exists,
2. `__slots__` is tuple or string,
3. all slot items are strings.

It is the fourth structural check in `verify_mixin_definition`.

## Diagnostic value
The error message includes:

- a list of all forbidden slot names,
- a clear explanation of why they are forbidden,
- actionable guidance for correction,
- recommended naming conventions.

This makes debugging fast, friendly, and predictable.

## Notes
- This is a pure `raise_...` function.
- It is used exclusively by the mixin definition validator.
- All mixins must pass this check before they can be applied to instances.
"""