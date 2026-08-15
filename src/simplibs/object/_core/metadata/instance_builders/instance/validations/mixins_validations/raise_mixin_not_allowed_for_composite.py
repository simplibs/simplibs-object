from typing import TYPE_CHECKING
# Outers
from .......exceptions import SimpleInitializationError
# Annotations
if TYPE_CHECKING:
    from ......protocols.classes import SimpleClassLike
    from ......protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_not_allowed_for_composite(
    cls: "SimpleClassLike",
    mixin: "SimpleMixinProtocol",
) -> None:
    """Raises an error when a constant-only mixin is applied to a composite instance."""

    raise SimpleInitializationError(
        error_name="INVALID MIXIN USAGE",
        label="mixin_constant_only_not_allowed_for_composite",
        expected="Mixin usable only for atomic (constant) instances",
        value=mixin,
        problem=(
            f"Mixin '{mixin.__name__}' is marked as _constant_only=True and "
            f"cannot be applied to composite class '{cls.__name__}'."
        ),
        context=f"create_instance(cls={cls.__name__}, mixin={mixin.__name__})",
        how_to_fix=(
            "Use this mixin only when creating atomic instances (as_atom=True).",
            "Example:",
            "    create_instance(MyClass, mixins=(MyMixin,), as_atom=True)",
            "",
            "If the mixin should support composite instances, remove the flag:",
            "    _constant_only = False",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_mixin_not_allowed_for_composite

## Purpose
Signals that a mixin marked with `_constant_only=True` was incorrectly applied to
a composite instance. Constant-only mixins are designed exclusively for atomic
nodes and cannot operate on composite structures.

## Behavior
- Triggered when:
  - `mixin._constant_only is True`
  - AND the target instance is composite (`is_atom=False`)
- Raises `SimpleInitializationError` with a clear diagnostic message and remediation steps.

## Notes
- Constant-only mixins typically assume a single-value topology and cannot
  interact with composite nodes that contain nested children.
- This validator enforces strict compatibility rules defined on `SimpleMixin`.
- Part of the five-rule compatibility matrix:
  - `_constant_only`
  - `_composite_only`
  - `_mutable_only`
  - `_immutable_only`
  - `_only_types`
"""