# 🧱 `Arithmetic` — Binary Arithmetic Operators

`Arithmetic` gives a SimpleObject the standard arithmetic operators (`+`, `-`, `*`,
`/`, `//`, `%`, `**`), including their reflected counterparts, so numeric-valued
instances behave like plain numbers in expressions. Every operator returns a **new**
instance and includes a lazy fallback type conversion when the raw operation fails.

```python
import operator
from numbers import Number
from ...core_mixins import NodesDicts, Snapshot
from ._utils import execute_arithmetic_op

class Arithmetic(NodesDicts, Snapshot):
    ...
```

`_only_types = Number` — every operation is delegated to Python's own arithmetic on
`self.value`.

---

## 🧭 Table of Contents

* [`__add__` / `__radd__`](#__add__--__radd__)
* [`__sub__` / `__rsub__`](#__sub__--__rsub__)
* [`__mul__` / `__rmul__`](#__mul__--__rmul__)
* [`__truediv__` / `__rtruediv__`](#__truediv__--__rtruediv__)
* [`__floordiv__` / `__rfloordiv__`](#__floordiv__--__rfloordiv__)
* [`__mod__` / `__rmod__`](#__mod__--__rmod__)
* [`__pow__` / `__rpow__`](#__pow__--__rpow__)

---

### `__add__` / `__radd__`

Returns a new instance with the value `self.value + other` (or `other + self.value`
for the reflected form).

**Parameters:**
* `other` (*Any*): a raw value or Simple instance.

**Returns:**
* a new instance holding the result.

**Example usage:**
```python
new_price = price + 10
new_price = 10 + price
```

**Under the hood:**
```python
def __add__(self, other):
    return execute_arithmetic_op(self, operator.add, other)

def __radd__(self, other):
    return execute_arithmetic_op(self, operator.add, other, is_reversed=True)
```

[▲ Back to top](#-table-of-contents)

---

### `__sub__` / `__rsub__`

Same shape as `__add__`/`__radd__`, using `operator.sub`.

**Parameters:**
* `other` (*Any*)

**Returns:**
* a new instance holding `self.value - other` (or reversed).

**Example usage:**
```python
new_price = price - 5
```

**Under the hood:**
```python
def __sub__(self, other):
    return execute_arithmetic_op(self, operator.sub, other)
```

[▲ Back to top](#-table-of-contents)

---

### `__mul__` / `__rmul__`

Same shape, using `operator.mul`.

**Parameters:**
* `other` (*Any*)

**Returns:**
* a new instance holding `self.value * other` (or reversed).

**Example usage:**
```python
double = price * 2
```

**Under the hood:**
```python
def __mul__(self, other):
    return execute_arithmetic_op(self, operator.mul, other)
```

[▲ Back to top](#-table-of-contents)

---

### `__truediv__` / `__rtruediv__`

Same shape, using `operator.truediv`.

**Parameters:**
* `other` (*Any*)

**Returns:**
* a new instance holding `self.value / other` (or reversed).

**Example usage:**
```python
half = price / 2
```

**Under the hood:**
```python
def __truediv__(self, other):
    return execute_arithmetic_op(self, operator.truediv, other)
```

[▲ Back to top](#-table-of-contents)

---

### `__floordiv__` / `__rfloordiv__`

Same shape, using `operator.floordiv`.

**Parameters:**
* `other` (*Any*)

**Returns:**
* a new instance holding `self.value // other` (or reversed).

**Example usage:**
```python
whole = price // 2
```

**Under the hood:**
```python
def __floordiv__(self, other):
    return execute_arithmetic_op(self, operator.floordiv, other)
```

[▲ Back to top](#-table-of-contents)

---

### `__mod__` / `__rmod__`

Same shape, using `operator.mod`.

**Parameters:**
* `other` (*Any*)

**Returns:**
* a new instance holding `self.value % other` (or reversed).

**Example usage:**
```python
remainder = price % 3
```

**Under the hood:**
```python
def __mod__(self, other):
    return execute_arithmetic_op(self, operator.mod, other)
```

[▲ Back to top](#-table-of-contents)

---

### `__pow__` / `__rpow__`

Same shape, using `operator.pow`.

**Parameters:**
* `other` (*Any*)

**Returns:**
* a new instance holding `self.value ** other` (or reversed).

**Example usage:**
```python
squared = price ** 2
```

**Under the hood:**
```python
def __pow__(self, other):
    return execute_arithmetic_op(self, operator.pow, other)
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../../README_MIXINS_OVERVIEW.md)
