from typing import TYPE_CHECKING, NoReturn
# Outers
from .....exceptions import SimpleMixinError
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_slots_is_not_defined(
    cls: "SimpleMixinProtocol",
) -> NoReturn:
    """
    Raises an error when a mixin does not define its own '__slots__'
    and instead inherits them from a parent class.
    """

    raise SimpleMixinError(
        error_name="MIXIN DEFINITION ERROR",
        label="__slots__",
        expected="Mixin must define its own __slots__ (not inherited).",
        value=cls.__name__,
        problem=(
            f"Mixin '{cls.__name__}' does not define its own '__slots__'. ",
            "Inherited slots are not allowed for mixins."
        ),
        context=f"Mixin definition check: {cls.__name__}",
        how_to_fix=(
            "Add an explicit __slots__ definition to the mixin.",
            "Example: __slots__ = ('my_attr',)",
            "Ensure that __slots__ are not inherited from a parent class.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_mixin_slots_is_not_defined

## Purpose
Ensures that every mixin explicitly declares its own `__slots__` attribute.  
Mixin classes must not inherit `__slots__` from parent classes, because mixins
participate in dynamic class composition and must provide a predictable,
self‑contained memory layout.

## Architectural reasoning
Mixins are injected into dynamically generated instance classes.  
If a mixin inherits `__slots__` from a parent class:

- the memory layout becomes ambiguous,
- slot collisions may occur,
- mixin validation cannot reliably determine the mixin’s structural footprint,
- debugging becomes significantly harder.

Requiring explicit `__slots__` guarantees that each mixin is structurally isolated
and safe to merge into composite runtime classes.

## Pipeline position
This function is called at the very beginning of `verify_mixin_definition`.  
It is the first structural check performed on a mixin class:

1. `__slots__` must exist in the class’s own `__dict__`.
2. If missing → this error is raised immediately.
3. No further validation steps are executed.

## Diagnostic value
The error message clearly states:

- which mixin failed,
- why the failure occurred,
- what the mixin is expected to define,
- how to fix the issue (including an example).

This makes the validation friendly, actionable, and easy to understand.

## Notes
- This is a pure `raise_...` function: it performs no conditional logic.
- It is used exclusively by the mixin definition validator.
- All mixins in the Simple system must pass this check.
"""