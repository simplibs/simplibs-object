from typing import TYPE_CHECKING
# Outers
from .......exceptions import SimpleMixinError
# Annotations
if TYPE_CHECKING:
    from ......protocols.classes import SimpleClassLike
    from ......protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_slots_conflict_error(
    cls: "SimpleClassLike",
    mixins: tuple["SimpleMixinProtocol", ...],
    error: TypeError,
) -> None:
    """Raises a structured error when a __slots__ collision occurs between mixins during class compilation."""

    mixin_names = ", ".join(m.__name__ for m in mixins)

    raise SimpleMixinError(
        error_name="MIXIN SLOTS CONFLICT",
        label="mixin_slots_conflict",
        expected="Mixins with non-overlapping __slots__ layouts",
        value=error,
        problem=(
            "A __slots__ layout mismatch occurred while compiling the instance type. "
            "Python raised a TypeError because two or more mixins define identical slot names "
            "or structurally incompatible memory layouts."
        ),
        context=f"create_instance(cls={cls.__name__}, mixins=({mixin_names}))",
        how_to_fix=(
            "Inspect __slots__ definitions across all attached mixins.",
            "Ensure that no two mixins declare the same slot field name.",
            "Example of a valid layout:",
            "    class MixinA(SimpleMixin):",
            "        __slots__ = ('a',)",
            "",
            "    class MixinB(SimpleMixin):",
            "        __slots__ = ('b',)",
            "",
            "If multiple mixins need to share state under the same slot name, "
            "consider merging them or refactoring the state propagation design.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_mixin_slots_conflict_error

## Purpose
Translates raw `TypeError` raised by `type()` during slot layout conflicts into a
structured `SimpleMixinError` with clear diagnostics and remediation steps.

## Behavior
- Triggered when dynamic class compilation (`type()`) fails due to incompatible
  `__slots__` layouts across mixins and the base class.
- Reports all mixins involved and suggests how to resolve the conflict.

## Notes
- Keeps `create_instance_class` minimal by delegating verbose error handling.
- Provides a domain-specific explanation instead of opaque C-level error text.
"""