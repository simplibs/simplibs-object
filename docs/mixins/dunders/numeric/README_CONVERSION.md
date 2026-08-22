# 🧱 `Conversion` — Native Python Numeric Conversion

`Conversion` lets a SimpleObject be converted to native Python numeric types —
`int(obj)`, `float(obj)`, `complex(obj)`, `round(obj)`, `math.floor(obj)`, etc. Unlike
the other numeric mixins, every method here returns a plain Python value, never a
SimpleObject.

```python
import math
from numbers import Number
from ...base_class import SimpleMixin
from ._utils import execute_conversion

class Conversion(SimpleMixin):
    ...
```

`_only_types = Number`.

---

## 🧭 Table of Contents

* [`__int__`](#__int__)
* [`__float__`](#__float__)
* [`__complex__`](#__complex__)
* [`__index__`](#__index__)
* [`__round__`](#__round__)
* [`__floor__` / `__ceil__` / `__trunc__`](#__floor__--__ceil__--__trunc__)

---

### `__int__`

Returns `int(self.value)`.

**Parameters:**
* *(none)*

**Returns:**
* `int`

**Example usage:**
```python
int(price)
```

**Under the hood:**
```python
def __int__(self):
    return execute_conversion(self, int)
```

[▲ Back to top](#-table-of-contents)

---

### `__float__`

Returns `float(self.value)`.

**Parameters:**
* *(none)*

**Returns:**
* `float`

**Example usage:**
```python
float(price)
```

**Under the hood:**
```python
def __float__(self):
    return execute_conversion(self, float)
```

[▲ Back to top](#-table-of-contents)

---

### `__complex__`

Returns `complex(self.value)`.

**Parameters:**
* *(none)*

**Returns:**
* `complex`

**Example usage:**
```python
complex(price)
```

**Under the hood:**
```python
def __complex__(self):
    return execute_conversion(self, complex)
```

[▲ Back to top](#-table-of-contents)

---

### `__index__`

Returns an exact `int` for use in `range()`, slicing, etc. Raises `TypeError` if the
value isn't already an `int`.

**Parameters:**
* *(none)*

**Returns:**
* `int`

**Example usage:**
```python
my_list[index_obj]
range(count_obj)
```

**Under the hood:**
```python
def __index__(self):
    value = self.value
    if not isinstance(value, int):
        raise TypeError(f"{self.meta.class_name} cannot be used as an index.")
    return value
```

[▲ Back to top](#-table-of-contents)

---

### `__round__`

Returns `round(self.value)` or `round(self.value, n)`.

**Parameters:**
* `n` (*int | None*, default `None`): number of digits.

**Returns:**
* `int | float`

**Example usage:**
```python
round(price)
round(price, 2)
```

**Under the hood:**
```python
def __round__(self, n=None):
    return (
        execute_conversion(self, round, n)
        if n is not None
        else execute_conversion(self, round)
    )
```

[▲ Back to top](#-table-of-contents)

---

### `__floor__` / `__ceil__` / `__trunc__`

Return `math.floor(self.value)`, `math.ceil(self.value)`, `math.trunc(self.value)`
respectively.

**Parameters:**
* *(none)*

**Returns:**
* `int`

**Example usage:**
```python
import math
math.floor(price)
math.ceil(price)
math.trunc(price)
```

**Under the hood:**
```python
def __floor__(self):
    return execute_conversion(self, math.floor)

def __ceil__(self):
    return execute_conversion(self, math.ceil)

def __trunc__(self):
    return execute_conversion(self, math.trunc)
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../../README_MIXINS_OVERVIEW.md)
