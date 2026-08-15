from typing import TYPE_CHECKING, Any
# Outers
from ...._common_logic.immutability import with_constant
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.dunders.numeric import BitwiseProtocol
    from ....._core.protocols.mixins.dunders.numeric.internal_types import Operator


def execute_bitwise_op(
    self: "BitwiseProtocol",
    operator: "Operator",
    other: Any,
    is_reversed: bool = False
) -> Any:
    """
    Modular executor for standard and right‑hand bitwise operations.
    """

    # 1. Extract second operand
    other_value = getattr(other, "value", other)

    # 2. Attempt computation with correct operand order
    try:
        value = (
            operator(other_value, self.value)
            if is_reversed
            else operator(self.value, other_value)
        )
        return with_constant(self, self.meta.name_snake, value)

    # 3. On failure, signal unsupported operation
    except TypeError:
        return NotImplemented


_DESIGN_NOTES = """
# execute_bitwise_op

## Purpose
Provides a unified executor for all bitwise dunder operations
(`__and__`, `__or__`, `__xor__`, `__lshift__`, `__rshift__`, `__invert__`,
and their reversed variants).

It ensures that bitwise operations:

- work seamlessly with both raw values and Simple instances,
- respect operand direction (normal vs reversed),
- return new immutable constant instances,
- behave consistently across all numeric bitwise mixins.

---

## Architectural Role
This helper is used internally by the Bitwise mixin to implement all bitwise dunders.

It provides:

- operand extraction,
- correct operator direction,
- composite‑constant creation,
- consistent fallback behavior.

It is the core bitwise engine for Simple numeric objects.

---

## Behavior

### 1. Operand extraction
Supports both:

- raw Python values (`int`, `bool`, …)
- Simple objects (`other.value`)

Resolved via:

```
other_value = getattr(other, "value", other)
```

### 2. Direct computation
Executes the operator in the correct direction:

- normal: `self.value OP other_value`
- reversed: `other_value OP self.value`

If successful, returns a new immutable constant instance:

```
with_constant(self, self.meta.name_snake, value)
```

Bitwise operations **never** use composite semantics — they always produce a
constant, because bitwise ops do not propagate through inner nodes.

### 3. Failure handling
If the operation raises `TypeError`, the function returns:

```
NotImplemented
```

This signals Python to try the reversed dunder or raise a proper error.

No type alignment is attempted — bitwise operations require strict operand
types and unsafe coercion would break semantics.

---

## Notes
- This function is internal and not part of the public API.
- It guarantees deterministic bitwise behavior across all numeric mixins.
- It keeps mixin implementations minimal and declarative.
- Bitwise operations intentionally avoid type alignment for safety.
"""