from typing import TYPE_CHECKING
# Outers
from .......exceptions import SimpleMixinError
# Annotations
if TYPE_CHECKING:
    from ......protocols.classes import SimpleClassLike
    from ......protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_not_support_default_value_type(
    cls: "SimpleClassLike",
    mixin: "SimpleMixinProtocol",
) -> None:
    """Raises an error when a mixin's _only_types constraint does not match the class default value."""

    default_value = cls.meta.default
    allowed_types = mixin._only_types

    raise SimpleMixinError(
        error_name="INVALID MIXIN USAGE",
        label="mixin_default_type_not_supported",
        expected=f"Default value of type {allowed_types}",
        value=default_value,
        problem=(
            f"Mixin '{mixin.__name__}' declares _only_types={allowed_types}, "
            f"but the default value of class '{cls.__name__}' is "
            f"{default_value!r} ({type(default_value).__name__})."
        ),
        context=f"create_instance(cls={cls.__name__}, mixin={mixin.__name__})",
        how_to_fix=(
            "Use this mixin only with classes whose default value matches the required types.",
            "Example:",
            "    class MyClass(SimpleObject):",
            "        _default = 10",
            "",
            "Or adjust the mixin to accept the desired type:",
            "    _only_types = (int, str)",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_mixin_not_support_default_value_type

## Purpose
Signals that a mixin with a declared `_only_types` constraint was applied to a
class whose default value does not match any of the allowed types.

## Behavior
- Triggered when:
  - `mixin._only_types is not UNSET`
  - AND `not isinstance(cls.meta.default, mixin._only_types)`
- Raises `SimpleMixinError` with a clear diagnostic message and remediation steps.

## Notes
- `_only_types` is a strong compatibility constraint used by mixins that operate
  only on specific value domains (e.g., numeric mixins, string mixins, tuple mixins).
- This validator ensures that mixins cannot be attached to incompatible classes,
  preventing runtime errors in mixin logic.
- Completes the five-rule compatibility matrix:
  - `_constant_only`
  - `_composite_only`
  - `_mutable_only`
  - `_immutable_only`
  - `_only_types`
"""