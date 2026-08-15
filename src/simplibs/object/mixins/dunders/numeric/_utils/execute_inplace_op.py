from typing import TYPE_CHECKING, Any
# Inners
from ._align_operand_type import _align_operand_type
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.dunders.numeric import InplaceProtocol
    from ....._core.protocols.mixins.dunders.numeric.internal_types import Operator


def execute_inplace_op(
    self: "InplaceProtocol",
    operator: "Operator",
    other: Any
) -> Any:
    """
    Fast modular executor for in‑place arithmetic operations.
    Extracts the operand, performs the computation, and safely writes the
    result into self.value. Includes fallback for safe type alignment.
    """

    # 1. Extract second operand
    other_value = getattr(other, "value", other)

    # 2. Attempt direct computation
    try:
        self.value = operator(self.value, other_value)
        return self

    # 3. Attempt safe type alignment
    except TypeError:

        # 3.1 Align operand type
        coerced = _align_operand_type(self, other_value)

        # 3.2 Retry computation
        try:
            self.value = operator(self.value, coerced)
            return self

        # 3.3 Failure or division by zero
        except (TypeError, ZeroDivisionError):
            return NotImplemented

    # 3.3 Division by zero in the first attempt
    except ZeroDivisionError:
        return NotImplemented


_DESIGN_NOTES = """
# execute_inplace_op

## Purpose
Provides the unified executor for all in‑place arithmetic dunder operations
(`__iadd__`, `__isub__`, `__imul__`, `__itruediv__`, `__ifloordiv__`,
`__imod__`, `__ipow__`).

It ensures that in‑place operations:

- mutate the instance value safely,
- support lazy fallback type alignment,
- behave consistently across all numeric mixins,
- correctly signal unsupported operations via `NotImplemented`.

---

## Architectural Role
This helper is used internally by the Inplace mixin to implement all in‑place arithmetic dunders.

It provides:

- operand extraction,
- safe type alignment,
- mutation of `self.value`,
- unified fallback behavior.

It is the core in‑place arithmetic engine for Simple numeric objects.

---

## Behavior

### 1. Operand extraction
Supports both:

- raw Python values (`int`, `float`, `Decimal`, …)
- Simple objects (`other.value`)

Resolved via:

```
other_value = getattr(other, "value", other)
```

### 2. Direct in‑place computation
Executes:

```
self.value = operator(self.value, other_value)
```

If successful, returns `self`.

### 3. Lazy fallback type alignment
If the operation fails with `TypeError`, the function attempts safe alignment:

```
coerced = _align_operand_type(self, other_value)
```

This allows operations like:

- `int += Decimal`
- `int *= Fraction`
- `int -= float`

but avoids unsafe conversions (e.g., `float → Decimal`).

### 4. Second attempt
The operator is retried with the aligned operand.

If it still fails, or if division by zero occurs, the function returns:

```
NotImplemented
```

This signals Python to fall back to the reversed in‑place dunder or raise an error.

### 5. Division by zero
Both attempts catch `ZeroDivisionError` and return `NotImplemented`.

---

## Notes
- This function is internal and not part of the public API.
- It guarantees deterministic in‑place arithmetic behavior across all numeric mixins.
- It keeps mixin implementations minimal and declarative.
- In‑place operations mutate the instance directly — unlike arithmetic ops, which return new composites.
"""