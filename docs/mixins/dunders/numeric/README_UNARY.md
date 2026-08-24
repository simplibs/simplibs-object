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

[⬅️ Back to Mixins Overview](../../../README_MIXINS_OVERVIEW.md)
