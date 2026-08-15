from typing import TYPE_CHECKING
# Outers
from .......exceptions import SimpleMixinError
# Annotations
if TYPE_CHECKING:
    from ......protocols.classes import SimpleClassLike
    from ......protocols.mixins.base_class import SimpleMixinProtocol


def validate_mixin_is_simple_base_subclass(
    cls: "SimpleClassLike",
    mixin: "SimpleMixinProtocol",
) -> None:
    """Validates that the mixin inherits from SimpleMixin."""

    from ........mixins.base_class import SimpleMixin

    # 1. Check inheritance
    if issubclass(mixin, SimpleMixin):
        return

    # 2. Raise error
    raise SimpleMixinError(
        error_name="INVALID MIXIN",
        label="mixin_not_subclass_of_simplemixin",
        expected="Subclass of SimpleMixin",
        value=mixin,
        problem=f"Class '{mixin.__name__}' does not inherit from SimpleMixin and cannot be used as a mixin for '{cls.__name__}'.",
        context=f"create_instance(cls={cls.__name__}, mixin={mixin.__name__})",
        how_to_fix=(
            "Ensure the mixin inherits from SimpleMixin.",
            "Example:",
            "    class MyMixin(SimpleMixin):",
            "        __slots__ = ()",
            "",
            "If the class is not intended to be a mixin, do not pass it to create_instance.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# validate_mixin_is_simple_base_subclass

## Purpose
Ensures that every mixin used in instance creation is a proper subclass of
`SimpleMixin`. This is required because mixins participate in inheritance,
slot merging, initialization hooks, and optional class‑extension mechanisms.

## Behavior
1. Imports `SimpleMixin` lazily to avoid circular dependencies.
2. Checks whether `mixin` is a subclass of `SimpleMixin`.
3. If not, raises `SimpleMixinError` with a clear remediation message.

## Notes
- This validator is the second gate in the mixin pipeline, following
  `validate_mixin_is_class`.
- Guarantees that only structurally valid mixins enter deeper compatibility
  checks (constant‑only, composite‑only, mutable‑only, immutable‑only, `_only_types`).
- Prevents accidental misuse of arbitrary classes as mixins.
"""