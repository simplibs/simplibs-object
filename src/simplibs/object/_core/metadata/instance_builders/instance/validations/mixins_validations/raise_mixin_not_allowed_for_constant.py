from typing import TYPE_CHECKING
# Outers
from .......exceptions import SimpleInitializationError
# Annotations
if TYPE_CHECKING:
    from ......protocols.classes import SimpleClassLike
    from ......protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_not_allowed_for_constant(
    cls: "SimpleClassLike",
    mixin: "SimpleMixinProtocol",
) -> None:
    """Raises an error when a composite-only mixin is applied to an atomic instance."""

    raise SimpleInitializationError(
        error_name="INVALID MIXIN USAGE",
        label="mixin_composite_only_not_allowed_for_constant",
        expected="Mixin usable only for composite instances",
        value=mixin,
        problem=(
            f"Mixin '{mixin.__name__}' is marked as _composite_only=True and "
            f"cannot be applied to atomic class '{cls.__name__}'."
        ),
        context=f"create_instance(cls={cls.__name__}, mixin={mixin.__name__})",
        how_to_fix=(
            "Use this mixin only when creating composite instances (as_atom=False).",
            "Example:",
            "    create_instance(MyClass, mixins=(MyMixin,), as_atom=False)",
            "",
            "If the mixin should support atomic instances, remove the flag:",
            "    _composite_only = False",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_mixin_not_allowed_for_constant

## Purpose
Signals that a mixin marked with `_composite_only=True` was incorrectly applied to
an atomic instance. Composite-only mixins assume a multi‑node structure and cannot
operate on atomic nodes.

## Behavior
- Triggered when:
  - `mixin._composite_only is True`
  - AND the target instance is atomic (`is_atom=True`)
- Raises `SimpleInitializationError` with a clear diagnostic message and remediation steps.

## Notes
- Composite-only mixins typically rely on child-node traversal, decomposition,
  or multi‑value logic that atomic nodes do not support.
- This validator enforces strict compatibility rules defined on `SimpleMixin`.
- Part of the five-rule compatibility matrix:
  - `_constant_only`
  - `_composite_only`
  - `_mutable_only`
  - `_immutable_only`
  - `_only_types`
"""