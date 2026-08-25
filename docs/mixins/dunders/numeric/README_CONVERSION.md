# 🧱 `Conversion` — Native Python Numeric Conversion

`Conversion` lets a SimpleObject be converted to native Python numeric types —
`int(obj)`, `float(obj)`, `complex(obj)`, `round(obj)`, `math.floor(obj)`, etc. Unlike
the other numeric mixins, every method here returns a plain Python value, never a
SimpleObject.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin

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
* [`execute_conversion`](#execute_conversion)

[⬅️ Back to main Mixins Overview](../../README_MIXINS_OVERVIEW.md)

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

### `execute_conversion`

Executes a native value conversion and provides a unified `TypeError`
message if the conversion fails.

**Parameters:**

* `self` — the current instance.
* `func` — the conversion function to execute.
* `*args` — additional arguments passed to the conversion function.

**Returns:**

* the converted value.

**Raises:**

* `TypeError` — if the conversion fails because of an invalid type or value.

**Example usage:**

```python
int(value)
```

**Under the hood:**

```python
def execute_conversion(
    self: "ConversionProtocol",
    func: Callable[..., Any],
    *args: Any
) -> Any:
    try:
        return func(self.value, *args)

    except (TypeError, ValueError) as e:
        raise TypeError(
            f"Cannot execute {func.__name__}() on {self.meta.class_name} "
            f"(value={self.value!r}): {e}"
        ) from e
```

[▲ Back to top](#-table-of-contents)

---

