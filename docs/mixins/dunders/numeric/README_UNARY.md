# 🧱 `Unary` — Unary Numeric Operators

`Unary` gives a SimpleObject the unary numeric operators — `-x`, `+x`, `abs(x)` — with
the same lazy fallback type conversion as `Arithmetic`. Every operator returns a new
instance.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin
from src.simplibs.object.mixins.core_mixins import NodesDicts, NodesTuple, Snapshot

class Unary(Snapshot, NodesDicts, NodesTuple, SimpleMixin):
    ...
```

`_only_types = Number`.

---

## 🧭 Table of Contents

* [`__neg__`](#__neg__)
* [`__pos__`](#__pos__)
* [`__abs__`](#__abs__)
* [`execute_unary_op`](#execute_unary_op)

[⬅️ Back to main Mixins Overview](../../README_MIXINS_OVERVIEW.md)

---

### `__neg__`

Returns a new instance with the value `-self.value`.

**Parameters:**
* *(none)*

**Returns:**
* a new instance.

**Example usage:**
```python
-price
```

**Under the hood:**
```python
def __neg__(self):
    return execute_unary_op(self, operator.neg)
```

[▲ Back to top](#-table-of-contents)

---

### `__pos__`

Returns a new instance with the value `+self.value`.

**Parameters:**
* *(none)*

**Returns:**
* a new instance.

**Example usage:**
```python
+price
```

**Under the hood:**
```python
def __pos__(self):
    return execute_unary_op(self, operator.pos)
```

[▲ Back to top](#-table-of-contents)

---

### `__abs__`

Returns a new instance with the value `abs(self.value)`.

**Parameters:**
* *(none)*

**Returns:**
* a new instance.

**Example usage:**
```python
abs(price)
```

**Under the hood:**
```python
def __abs__(self):
    return execute_unary_op(self, abs)
```

[▲ Back to top](#-table-of-contents)

---

### `execute_unary_op`

Executes a unary numeric operation and returns a new instance with the
calculated value. If the operation initially fails due to an operand type
mismatch, it attempts safe type alignment before returning `NotImplemented`.

**Parameters:**

* `self` — the current instance.
* `operator` — the unary operator to execute.

**Returns:**

* a new instance with the calculated value.
* `NotImplemented` if the operation cannot be performed.

**Example usage:**

```python
-price
```

**Under the hood:**

```python
def execute_unary_op(
    self: "UnaryProtocol",
    operator: "UnaryOperator"
) -> Any:
    try:
        return with_composite(self, self.meta.name_snake, operator(self.value))

    except TypeError:
        coerced = _align_operand_type(self, self.value)

        try:
            return with_composite(
                self,
                self.meta.name_snake,
                operator(coerced)
            )

        except TypeError:
            return NotImplemented
```

[▲ Back to top](#-table-of-contents)

---

