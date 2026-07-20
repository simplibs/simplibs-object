from typing import TYPE_CHECKING
# Outers
from .......exceptions import SimpleMixinError
# Annotations
if TYPE_CHECKING:
    from .......protocols.classes import SimpleClassLike
    from .......protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_slots_conflict_error(
    cls: "SimpleClassLike",
    mixins: tuple["SimpleMixinProtocol", ...],
    error: TypeError
) -> None:
    """Raises a structured error when a `__slots__` collision occurs between mixins during class compilation.

    Triggered dynamically when `type()` compilation catches a low-level C-layout allocation mismatch.
    """

    mixin_names = ", ".join(m.__name__ for m in mixins)

    raise SimpleMixinError(
        error_name="MIXIN SLOTS CONFLICT",
        label="Slot name collision between mixins",
        expected="Mixins containing non-overlapping __slots__ layouts.",
        value=error,
        problem=(
            "A layout layout mismatch occurred within __slots__ allocation while compiling the instance type. "
            "Python raised a TypeError because two or more mixins define identical slot identifiers "
            "or possess structurally incompatible memory layouts."
        ),
        context=(
            f"create_instance(cls={cls.__name__}, mixins=({mixin_names}))"
        ),
        how_to_fix=(
            "Inspect the __slots__ definitions across all attached mixin dependencies.",
            "Ensure that no two distinct mixin layers declare duplicate slot field names.",
            "Example of a valid layout:",
            "    class MixinA(SimpleMixin):",
            "        __slots__ = ('a',)",
            "",
            "    class MixinB(SimpleMixin):",
            "        __slots__ = ('b',)",
            "",
            "If separate mixins share state logic requiring identical slot names, "
            "consider merging them or refactoring the state propagation design.",
        ),
        exception=TypeError
    )


_DESIGN_NOTES = """
# raise_mixin_slots_conflict_error

## Purpose
Provides an expressive error boundary that intercepts and translates raw, opaque Python C-level layout TypeErrors into structured, actionable domain exceptions.

## Architectural Design Decisions

### 1. Low-Level MRO Exception Translation
* Python's `type()` raises a generic `TypeError` with sparse information when layout allocations collide. This handler formats the internal context into a domain-specific `SimpleMixinError` for rapid debugging.

### 2. Isolation of Formatting and Diagnosis
* By moving complex multi-line text and mitigation steps into a separate utility function, the main `create_instance_class` pathway remains fast and free of verbose error-handling text overhead.
"""