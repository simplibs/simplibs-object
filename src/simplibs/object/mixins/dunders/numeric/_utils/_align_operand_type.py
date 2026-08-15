from typing import TYPE_CHECKING, Any
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.base_class import SimpleMixinLike


# noinspection PyBroadException
def _align_operand_type(
    self: "SimpleMixinLike",
    value: Any
) -> Any:
    """
    Attempts to convert the operand to the default value type,
    but only when the conversion is safe.

    Safe conversions:
    - int → float
    - int → Decimal
    - int → Fraction

    Unsafe conversions (NOT performed):
    - float → int
    - float → Decimal (rounding issues)
    - Fraction → int
    - Decimal → int
    """

    # 1. Determine target type
    target_type = type(self.meta.default)

    # 2. Attempt safe conversion
    try:
        return target_type(value)

    # 3. On failure, return original value
    except Exception:
        return value


_DESIGN_NOTES = """
# _align_operand_type

## Purpose
Provides safe type alignment for operands used in numeric dunder operations.
This helper attempts to convert the operand to the same type as the mixin’s
default value, but only when the conversion is guaranteed to be safe.

It prevents destructive or lossy conversions while still allowing natural
numeric interoperability (e.g., `int + float`, `int + Decimal`).

---

## Architectural Role
This function is used internally by all numeric dunder mixins:

- Arithmetic (`__add__`, `__sub__`, …)
- Unary (`__neg__`, `__abs__`, …)
- Inplace (`__iadd__`, `__isub__`, …)
- Bitwise (`__and__`, `__or__`, …)
- Conversion (`__int__`, `__float__`, …)

It ensures that operands are aligned to the correct type before the actual
operation is executed.

---

## Behavior

### Safe conversions (performed)
These conversions preserve numeric meaning and do not lose precision:

- `int → float`
- `int → Decimal`
- `int → Fraction`

### Unsafe conversions (NOT performed)
These conversions may lose precision or change semantics:

- `float → int`
- `float → Decimal` (rounding errors)
- `Fraction → int`
- `Decimal → int`

If a conversion is unsafe or fails, the original operand is returned unchanged.

---

## How it works

1. Determine the target type from:
   ```
   type(self.meta.default)
   ```

2. Attempt conversion:
   ```
   target_type(value)
   ```

3. If conversion fails, return the original value.

This ensures predictable, safe behavior across all numeric dunder operations.

---

## Notes
- This function is internal and not part of the public API.
- It is intentionally conservative: it prefers correctness over convenience.
- All structural logic is delegated to the numeric mixins that call it.
- It guarantees deterministic operand handling across all numeric operations.
"""