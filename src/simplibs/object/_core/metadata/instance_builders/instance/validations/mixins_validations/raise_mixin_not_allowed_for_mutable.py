from typing import TYPE_CHECKING
# Outers
from .......exceptions import SimpleInitializationError
# Annotations
if TYPE_CHECKING:
    from ......protocols.classes import SimpleClassLike
    from ......protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_not_allowed_for_mutable(
    cls: "SimpleClassLike",
    mixin: "SimpleMixinProtocol",
) -> None:
    """Raises an error when an immutable-only mixin is applied to a mutable instance."""

    raise SimpleInitializationError(
        error_name="INVALID MIXIN USAGE",
        label="mixin_immutable_only_not_allowed_for_mutable",
        expected="Mixin usable only for immutable instances",
        value=mixin,
        problem=(
            f"Mixin '{mixin.__name__}' is marked as _immutable_only=True and "
            f"cannot be applied to mutable class '{cls.__name__}'."
        ),
        context=f"create_instance(cls={cls.__name__}, mixin={mixin.__name__})",
        how_to_fix=(
            "Use this mixin only when creating immutable instances (mutable=False).",
            "Example:",
            "    create_instance(MyClass, mixins=(MyMixin,), mutable=False)",
            "",
            "If the mixin should support mutable instances, remove the flag:",
            "    _immutable_only = False",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_mixin_not_allowed_for_mutable

## Purpose
Signals that a mixin marked with `_immutable_only=True` was incorrectly applied to
a mutable instance. Immutable-only mixins assume that the instance has a fixed,
non‑changing value and does not support mutation or reactive recalculation.

## Behavior
- Triggered when:
  - `mixin._immutable_only is True`
  - AND the target instance is mutable (`mutable=True`)
- Raises `SimpleInitializationError` with a clear diagnostic message and remediation steps.

## Notes
- Immutable-only mixins typically rely on stable, non‑changing state semantics.
- This validator enforces strict compatibility rules defined on `SimpleMixin`.
- Part of the five-rule compatibility matrix:
  - `_constant_only`
  - `_composite_only`
  - `_mutable_only`
  - `_immutable_only`
  - `_only_types`
"""