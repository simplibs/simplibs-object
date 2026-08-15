from typing import TYPE_CHECKING, Any, Callable
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.dunders.numeric import ConversionProtocol


def execute_conversion(
    self: "ConversionProtocol",
    func: Callable[..., Any],
    *args: Any
) -> Any:
    """
    Fast modular executor for native value conversions.
    Performs the transformation and formats a unified error message on failure.
    """

    # 1. Attempt conversion
    try:
        return func(self.value, *args)

    # 2. Raise unified error on failure
    except (TypeError, ValueError) as e:
        raise TypeError(
            f"Cannot execute {func.__name__}() on {self.meta.class_name} "
            f"(value={self.value!r}): {e}"
        ) from e


_DESIGN_NOTES = """
# execute_conversion

## Purpose
Provides a unified, minimal, and safe executor for all numeric conversion
dunder methods (`__int__`, `__float__`, `__complex__`, `__round__`,
`__floor__`, `__ceil__`, `__trunc__`).

It ensures that conversions:

- call the correct native Python conversion function,
- propagate errors in a controlled and consistent way,
- produce a clear diagnostic message tied to the Simple object system.

---

## Architectural Role
This helper is used internally by the Conversion mixin to implement all conversion dunders.

It provides:

- a single point of execution for conversion logic,
- unified error formatting,
- consistent behavior across all numeric types.

It is intentionally minimal — conversion dunders must behave exactly like
native Python conversions, without fallback coercion or type alignment.

---

## Behavior

### 1. Direct conversion
The function calls:

```
func(self.value, *args)
```

where `func` is one of:

- `int`
- `float`
- `complex`
- `round`
- `math.floor`
- `math.ceil`
- `math.trunc`

This ensures full compatibility with Python’s numeric protocol.

### 2. Unified error handling
If the conversion fails with `TypeError` or `ValueError`, the function raises:

```
TypeError("Cannot execute func() on ClassName (value=...): original_error")
```

This provides:

- consistent formatting,
- clear context,
- correct exception type,
- proper chaining (`from e`).

### 3. No fallback conversion
Unlike arithmetic operations, conversion dunders **never** attempt type
alignment or coercion.

Conversions must be strict and predictable.

---

## Notes
- This function is internal and not part of the public API.
- It guarantees deterministic conversion behavior across all numeric mixins.
- It keeps mixin implementations minimal and declarative.
- Conversion errors always use `TypeError`, matching Python’s native behavior.
"""