from typing import TYPE_CHECKING, Any
# Outers
from ...._commons.immutability import with_composite
# Inners
from ._align_operand_type import _align_operand_type
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.dunders.numeric import UnaryProtocol
    from ....._core.protocols.mixins.dunders.numeric.internal_types import UnaryOperator


def execute_unary_op(
    self: "UnaryProtocol",
    operator: "UnaryOperator"
) -> Any:
    """
    Fast modular executor for unary numeric operations.
    Applies the operator to self.value and returns a new instance via
    with_composite. Includes fallback for safe type alignment.
    """

    # 1. Attempt direct computation
    try:
        return with_composite(self, self.meta.name_snake, operator(self.value))

    # 2. Attempt safe type alignment
    except TypeError:

        # 2.1 Align operand type
        coerced = _align_operand_type(self, self.value)

        # 2.2 Retry computation
        try:
            return with_composite(self, self.meta.name_snake, operator(coerced))

        # 2.3 Give up if still invalid
        except TypeError:
            return NotImplemented


_DESIGN_NOTES = """
# execute_unary_op

## Purpose
Provides the unified executor for all unary numeric dunder operations
(`__neg__`, `__pos__`, `__abs__`).  
It ensures that unary operations:

- apply the operator safely,
- support lazy fallback type alignment,
- return new composite instances,
- behave consistently across all numeric mixins.

---

## Architectural Role
This helper is used internally by the Unary mixin to implement all unary dunders.

It provides:

- operand extraction (always `self.value`),
- safe type alignment,
- composite instance creation,
- unified fallback behavior.

It is the core unary engine for Simple numeric objects.

---

## Behavior

### 1. Direct unary computation
Executes:

```
operator(self.value)
```

If successful, returns a new composite instance:

```
with_composite(self, self.meta.name_snake, result)
```

Unary operations **always** produce composites — they propagate through inner
nodes exactly like arithmetic operations.

### 2. Lazy fallback type alignment
If the operation fails with `TypeError`, the function attempts safe alignment:

```
coerced = _align_operand_type(self, self.value)
```

This allows operations like:

- `-Decimal(int_value)`
- `abs(Fraction(int_value))`
- `+float(int_value)`

but avoids unsafe conversions (e.g., `float → Decimal`).

### 3. Second attempt
The operator is retried with the aligned operand.

If it still fails, the function returns:

```
NotImplemented
```

This signals Python to fall back to alternative resolution or raise an error.

---

## Notes
- This function is internal and not part of the public API.
- It guarantees deterministic unary behavior across all numeric mixins.
- It keeps mixin implementations minimal and declarative.
- Unary operations never mutate the instance — they always return a new composite.
"""