from typing import TYPE_CHECKING, Any
# Outers
from ...._commons.immutability import with_composite
# Inners
from ._align_operand_type import _align_operand_type
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.dunders.numeric import ArithmeticProtocol
    from ....._core.protocols.mixins.dunders.numeric.internal_types import Operator


def execute_arithmetic_op(
    self: "ArithmeticProtocol",
    operator: "Operator",
    other: Any,
    *,
    is_reversed: bool = False
) -> Any:
    """
    Modular executor for standard and right‑hand arithmetic operations.
    """

    # 1. Extract second operand
    other_value = getattr(other, "value", other)

    # 2. Attempt direct computation and create a new instance
    try:
        value = (
            operator(other_value, self.value)
            if is_reversed
            else operator(self.value, other_value)
        )
        return with_composite(self, self.meta.name_snake, value)

    # 3. Attempt safe type alignment on failure
    except TypeError:

        # 3.1 Align operand type
        coerced = _align_operand_type(self, other_value)

        # 3.2 Retry computation with aligned operand
        try:
            value = (
                operator(coerced, self.value)
                if is_reversed
                else operator(self.value, coerced)
            )
            return with_composite(self, self.meta.name_snake, value)

        # 3.3 Give up if still invalid
        except TypeError:
            return NotImplemented


_DESIGN_NOTES = """
# execute_arithmetic_op

## Purpose
Provides a unified, modular executor for all arithmetic dunder operations
(`__add__`, `__sub__`, `__mul__`, `__truediv__`, `__floordiv__`, `__mod__`,
`__pow__`, and their reversed variants).

It ensures that arithmetic operations:

- work seamlessly with both raw values and Simple instances,
- support lazy fallback type alignment,
- return new composite instances,
- behave consistently across all numeric mixins.

---

## Architectural Role
This helper is used internally by the Arithmetic mixin to implement all arithmetic dunders.

It provides:

- operand extraction,
- safe type alignment,
- reversed‑operation support,
- composite instance creation.

It is the core arithmetic engine for Simple numeric objects.

---

## Behavior

### 1. Operand extraction
The function supports both:

- raw Python values (`int`, `float`, `Decimal`, …)
- Simple objects (`other.value`)

It resolves the operand via:

```
other_value = getattr(other, "value", other)
```

### 2. Direct computation
The operator is executed in the correct direction:

- normal: `self.value OP other_value`
- reversed: `other_value OP self.value`

If successful, a new composite instance is created using:

```
with_composite(self, self.meta.name_snake, value)
```

### 3. Lazy fallback type alignment
If the operation fails with `TypeError`, the function attempts safe alignment:

```
coerced = _align_operand_type(self, other_value)
```

This allows operations like:

- `int + Decimal`
- `int + Fraction`
- `int + float`

but avoids unsafe conversions (e.g., `float → Decimal`).

### 4. Second attempt
The operator is retried with the aligned operand.

If it still fails, the function returns:

```
NotImplemented
```

which correctly signals Python to try the reversed dunder or raise an error.

---

## Notes
- This function is internal and not part of the public API.
- It guarantees deterministic arithmetic behavior across all numeric mixins.
- It centralizes error handling, type alignment, and composite creation.
- It keeps mixin implementations minimal and declarative.
"""