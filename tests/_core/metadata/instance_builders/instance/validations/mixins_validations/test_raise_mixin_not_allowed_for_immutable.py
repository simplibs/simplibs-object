from typing import TYPE_CHECKING
# Outers
from .......exceptions import SimpleMixinError
# Annotations
if TYPE_CHECKING:
    from ......protocols.classes import SimpleClassLike
    from ......protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_not_allowed_for_immutable(
    cls: "SimpleClassLike",
    mixin: "SimpleMixinProtocol",
) -> None:
    """Raises an error when a mutable-only mixin is applied to an immutable instance."""

    raise SimpleMixinError(
        error_name="INVALID MIXIN USAGE",
        label="mixin_mutable_only_not_allowed_for_immutable",
        expected="Mixin usable only for mutable instances",
        value=mixin,
        problem=(
            f"Mixin '{mixin.__name__}' is marked as _mutable_only=True and "
            f"cannot be applied to immutable class '{cls.__name__}'."
        ),
        context=f"create_instance(cls={cls.__name__}, mixin={mixin.__name__})",
        how_to_fix=(
            "Use this mixin only when creating mutable instances (mutable=True).",
            "Example:",
            "    create_instance(MyClass, mixins=(MyMixin,), mutable=True)",
            "",
            "If the mixin should support immutable instances, remove the flag:",
            "    _mutable_only = False",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_mixin_not_allowed_for_immutable

## Purpose
Signals that a mixin marked with `_mutable_only=True` was incorrectly applied to
an immutable instance. Mutable-only mixins assume that the instance supports
state changes and reactive recalculation, which immutable nodes forbid.

## Behavior
- Triggered when:
  - `mixin._mutable_only is True`
  - AND the target instance is immutable (`mutable=False`)
- Raises `SimpleMixinError` with a clear diagnostic message and remediation steps.

## Notes
- Mutable-only mixins typically rely on mutation hooks, reactive bubbling, or
  dynamic state updates that immutable nodes cannot perform.
- This validator enforces strict compatibility rules defined on `SimpleMixin`.
- Part of the five-rule compatibility matrix:
  - `_constant_only`
  - `_composite_only`
  - `_mutable_only`
  - `_immutable_only`
  - `_only_types`
"""