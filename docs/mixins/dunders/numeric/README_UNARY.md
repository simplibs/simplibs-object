# 🧱 `Unary` — Unary Numeric Operators

`Unary` gives a SimpleObject the unary numeric operators — `-x`, `+x`, `abs(x)` — with
the same lazy fallback type conversion as `Arithmetic`. Every operator returns a new
instance.

```python
import operator
from numbers import Number
from ...core_mixins import NodesDicts, Snapshot
from ._utils import execute_unary_op

class Unary(NodesDicts, Snapshot):
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
