from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleInitializationError
# Annotations
if TYPE_CHECKING:
    from .......protocols.classes import SimpleClassLike


def validate_mixin_is_class(
    cls: "SimpleClassLike",
    mixin: object,
) -> None:
    """Validates that the mixin is a class object."""

    # 1. Check class identity
    if isinstance(mixin, type):
        return

    # 2. Raise error
    raise SimpleInitializationError(
        error_name="INVALID MIXIN",
        label="mixin_not_class",
        expected="Class derived from SimpleMixin",
        value=mixin,
        problem=f"Object '{mixin!r}' is not a class and cannot be used as a mixin for '{cls.__name__}'.",
        context=f"create_instance(cls={cls.__name__}, mixin={mixin!r})",
        how_to_fix=(
            "Pass a class, not an instance or other object.",
            "Correct usage:",
            "    create_instance(MyClass, mixins=(MyMixin,), as_atom=False)",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# validate_mixin_is_class

## Purpose
Ensures that every mixin passed to the instance‑builder is a valid class object.
Mixins must be classes because they participate in inheritance, slot merging,
and optional class‑extension hooks.

## Behavior
1. Checks whether `mixin` is an instance of `type`.
2. If not, raises `SimpleInitializationError` with a clear remediation message.

## Notes
- Mixins cannot be instances, functions, modules, or any other object type.
- This validator is the first gate in the mixin pipeline and prevents invalid
objects from entering deeper compatibility checks.
- Guarantees deterministic behavior for subsequent validators:
  - `validate_mixin_is_simple_base_subclass`
  - structural flags (`_constant_only`, `_composite_only`, …)
  - `_only_types` compatibility
"""