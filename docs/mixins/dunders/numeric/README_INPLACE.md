# 🧱 `Inplace` — In-Place Arithmetic Operators

`Inplace` gives a mutable SimpleObject the in-place arithmetic operators (`+=`, `-=`,
`*=`, `/=`, `//=`, `%=`, `**=`). Unlike `Arithmetic`, these genuinely mutate the
instance's own value via the normal validation/reactivity pipeline, and return `self`.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin

class Inplace(SimpleMixin):
    ...
```

`_mutable_only = True`, `_only_types = Number`.

---

## 🧭 Table of Contents

* [`__iadd__`](#__iadd__)
* [`__isub__`](#__isub__)
* [`__imul__`](#__imul__)
* [`__itruediv__`](#__itruediv__)
* [`__ifloordiv__`](#__ifloordiv__)
* [`__imod__`](#__imod__)
* [`__ipow__`](#__ipow__)
* [`execute_inplace_op`](#execute_inplace_op)

[⬅️ Back to main Mixins Overview](../../README_MIXINS_OVERVIEW.md)

---

### `__iadd__`

Mutates `self.value += other` in place.

**Parameters:**
* `other` (*Any*)

**Returns:**
* `self`

**Example usage:**
```python
price += 10
```

**Under the hood:**
```python
def __iadd__(self, other):
    return execute_inplace_op(self, operator.add, other)
```

[▲ Back to top](#-table-of-contents)

---

### `__isub__`

Mutates `self.value -= other` in place. Same shape as `__iadd__`, using
`operator.sub`.

**Example usage:**
```python
price -= 5
```

**Under the hood:**
```python
def __isub__(self, other):
    return execute_inplace_op(self, operator.sub, other)
```

[▲ Back to top](#-table-of-contents)

---

### `__imul__`

Mutates `self.value *= other` in place. Same shape, using `operator.mul`.

**Example usage:**
```python
price *= 2
```

**Under the hood:**
```python
def __imul__(self, other):
    return execute_inplace_op(self, operator.mul, other)
```

[▲ Back to top](#-table-of-contents)

---

### `__itruediv__`

Mutates `self.value /= other` in place. Same shape, using `operator.truediv`.

**Example usage:**
```python
price /= 2
```

**Under the hood:**
```python
def __itruediv__(self, other):
    return execute_inplace_op(self, operator.truediv, other)
```

[▲ Back to top](#-table-of-contents)

---

### `__ifloordiv__`

Mutates `self.value //= other` in place. Same shape, using `operator.floordiv`.

**Example usage:**
```python
price //= 2
```

**Under the hood:**
```python
def __ifloordiv__(self, other):
    return execute_inplace_op(self, operator.floordiv, other)
```

[▲ Back to top](#-table-of-contents)

---

### `__imod__`

Mutates `self.value %= other` in place. Same shape, using `operator.mod`.

**Example usage:**
```python
price %= 3
```

**Under the hood:**
```python
def __imod__(self, other):
    return execute_inplace_op(self, operator.mod, other)
```

[▲ Back to top](#-table-of-contents)

---

### `__ipow__`

Mutates `self.value **= other` in place. Same shape, using `operator.pow`.

**Example usage:**
```python
price **= 2
```

**Under the hood:**
```python
def __ipow__(self, other):
    return execute_inplace_op(self, operator.pow, other)
```

[▲ Back to top](#-table-of-contents)

---

### `execute_inplace_op`

Executes an in-place arithmetic operation, safely writes the resulting value
back into `self.value`, and returns the current instance. If the operands
cannot be aligned or the operation fails, it returns `NotImplemented`.

**Parameters:**

* `self` — the current instance.
* `operator` — the arithmetic operator to execute.
* `other` — the second operand.

**Returns:**

* `self` with the updated value.
* `NotImplemented` if the operation cannot be performed.

**Example usage:**

```python
price += tax
```

**Under the hood:**

```python
def execute_inplace_op(
    self: "InplaceProtocol",
    operator: "Operator",
    other: Any
) -> Any:
    other_value = getattr(other, "value", other)

    try:
        self.value = operator(self.value, other_value)
        return self

    except TypeError:
        coerced = _align_operand_type(self, other_value)

        try:
            self.value = operator(self.value, coerced)
            return self

        except (TypeError, ZeroDivisionError):
            return NotImplemented

    except ZeroDivisionError:
        return NotImplemented
```

[▲ Back to top](#-table-of-contents)

---
