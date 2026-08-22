from typing import TYPE_CHECKING, NoReturn
# Outers
from ...._common_logic.constants import RESTRICTION_FLAGS
from .....exceptions import SimpleRuntimeError
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_flag_is_not_bool(
    cls: "SimpleMixinProtocol",
) -> NoReturn:
    """
    Raises an error when one or more declarative mixin flags are not boolean.
    """

    # 1. Collect all invalid flags
    invalid_items = tuple(
        (flag, cls.__dict__[flag])
        for flag in RESTRICTION_FLAGS
        if flag in cls.__dict__ and not isinstance(cls.__dict__[flag], bool)
    )

    # 2. Raise structured error
    raise SimpleRuntimeError(
        error_name="MIXIN DEFINITION ERROR",
        label="Invalid mixin flag types",
        expected="All mixin flags must be boolean (True/False).",
        value=invalid_items,
        problem=(
            f"Mixin '{cls.__name__}' defines one or more flags with invalid types:",
            *[
                f"• {name} = {value!r} (type: {type(value).__name__})"
                for name, value in invalid_items
            ],
            "All declarative mixin flags must be boolean values.",
        ),
        context=f"Mixin definition check: {cls.__name__}",
        how_to_fix=(
            "Set each mixin flag to either True or False.",
            "Example: _constant_only = True",
            "Example: _mutable_only = False",
            "If a flag is not needed, remove it from the mixin.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_mixin_flag_is_not_bool

## Purpose
Validates that all declarative mixin flags are boolean values.  
These flags define structural compatibility constraints and must always be
explicitly set to `True` or `False`.

Supported flags:

- `_constant_only`
- `_composite_only`
- `_mutable_only`
- `_immutable_only`

## Architectural reasoning
Mixin flags participate in the instance‑builder pipeline.  
Incorrect flag types (e.g., strings, integers, objects) would break:

- mixin compatibility checks,
- structural resolution,
- mutability/immutability constraints,
- constant/composite mode selection.

Boolean values are required to keep the pipeline deterministic and predictable.

## Self-contained error logic
The main validation pipeline (`verify_mixin_definition`) remains clean and simple.
If any flag is invalid, the pipeline delegates to this error function.

The error function:

1. re-imports `RESTRICTION_FLAGS`,
2. scans the mixin class dictionary,
3. collects all invalid flags,
4. raises a structured error.

This ensures that the pipeline stays minimal while the error function handles
all diagnostic responsibilities.

## Multi‑flag reporting
A mixin may define multiple invalid flags at once.  
Reporting only the first invalid flag would force the developer into a slow,
iterative debugging cycle.

To prevent this, the validator reports **all invalid flags** in a single
structured error message.

## Pipeline position
This check occurs after verifying:

1. `__slots__` exists,
2. `__slots__` is tuple or string,
3. all slot items are strings,
4. no forbidden slot names are used.

It is the fifth structural check in `verify_mixin_definition`.

## Diagnostic value
The error message includes:

- a list of all invalid flags,
- their actual values,
- their types,
- clear expectations,
- actionable guidance for correction.

This makes debugging fast, friendly, and predictable.

## Notes
- This is a pure `raise_...` function.
- It is used exclusively by the mixin definition validator.
- All mixins must pass this check before they can be applied to instances.
"""