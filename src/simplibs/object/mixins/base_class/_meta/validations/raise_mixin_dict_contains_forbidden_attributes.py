from typing import TYPE_CHECKING, NoReturn
# Outers
from ...._common_logic.constants import FORBIDDEN_NAMES
from .....exceptions import SimpleRuntimeError
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_dict_contains_forbidden_attributes(
    cls: "SimpleMixinProtocol",
) -> NoReturn:
    """
    Raises an error when the mixin class defines forbidden attribute names
    in its class-level namespace (cls.__dict__).
    """

    forbidden_found = FORBIDDEN_NAMES & cls.__dict__.keys()
    forbidden_list = tuple(sorted(forbidden_found))

    raise SimpleRuntimeError(
        error_name="MIXIN DEFINITION ERROR",
        label="Forbidden class attributes",
        expected="Mixin class must not define attributes reserved by the Simple system.",
        value=forbidden_list,
        problem=(
            f"Mixin '{cls.__name__}' defines forbidden class-level attributes:",
            *[f"• {name}" for name in forbidden_list],
            "These names are reserved for internal Simple system mechanics.",
        ),
        context=f"Mixin definition check: {cls.__name__}",
        how_to_fix=(
            "Remove all forbidden attribute names from the mixin class.",
            "Use unique, non-conflicting attribute identifiers.",
            "Recommended: prefix mixin attributes with '_mx_' or '_mixin_'.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_mixin_dict_contains_forbidden_attributes

## Purpose
Validates that the mixin class does not define forbidden attribute names in its
class-level namespace (`cls.__dict__`). These names are reserved for internal
Simple system mechanics and must never be overridden by user-defined mixins.

## Architectural reasoning
The Simple system relies on several class-level attributes to manage:

- metadata access (`meta`, `__metadata__`)
- value access (`value`, `_value`)
- ownership (`owner`, `_owner`)
- composite structure (`_inners`)
- reactive recalculation (`_recalculate_self`, `_recalculate_inners`)
- logic evaluation (`_logic`)
- decomposition (`_decompose`)

If a mixin defines any of these names at the class level, it would:

- override internal API,
- break metadata resolution,
- shadow core properties,
- corrupt instance behavior,
- cause unpredictable runtime failures.

Therefore, strict enforcement is required.

## Why this check is separate from forbidden slot names
This validation checks **class-level attributes** declared in `cls.__dict__`.

A separate validation step checks **instance-level attributes** declared in
`__slots__`. These two checks serve different architectural layers and must
remain independent.

## Pipeline position
This check occurs after verifying:

1. `__slots__` exists,
2. `__slots__` is tuple or string,
3. all slot items are strings,
4. no forbidden slot names are used.

It is the fifth structural check in `verify_mixin_definition`.

## Diagnostic value
The error message includes:

- a list of all forbidden class-level names,
- a clear explanation of why they are forbidden,
- actionable guidance for correction,
- recommended naming conventions.

This makes debugging fast, friendly, and predictable.

## Notes
- This is a pure `raise_...` function.
- It is used exclusively by the mixin definition validator.
- All mixins must pass this check before they can be applied to instances.
"""