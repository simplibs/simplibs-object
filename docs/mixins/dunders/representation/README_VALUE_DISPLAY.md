# 🧱 `ValueDisplay` — Value-Like Printing

`ValueDisplay` overrides `__repr__` and `__str__` so an atomic instance presents
itself as the raw value it wraps — `print(price)` shows `19.99`, not a generic object
representation. Opt-in, intended for "value object" types like `Decimal`, `UUID`,
`PhoneNumber`.

```python
from ...base_class import SimpleMixin

class ValueDisplay(SimpleMixin):
    ...
```

`_constant_only = True`.

---

## 🧭 Table of Contents

* [`__repr__`](#__repr__)
* [`__str__`](#__str__)

---

### `__repr__`

Returns `ClassName(value_repr)` — keeps the class identity visible while showing the
wrapped value's own `repr()`.

**Parameters:**
* *(none)*

**Returns:**
* `str`

**Example usage:**
```python
repr(price)  # "Price(19.99)"
```

**Under the hood:**
```python
def __repr__(self) -> str:
    return f"{self.meta.class_name}({self.value!r})"
```

[▲ Back to top](#-table-of-contents)

---

### `__str__`

Returns just `str(self.value)` — drops the class name entirely.

**Parameters:**
* *(none)*

**Returns:**
* `str`

**Example usage:**
```python
print(price)  # "19.99"
```

**Under the hood:**
```python
def __str__(self) -> str:
    return str(self.value)
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../../README_MIXINS_OVERVIEW.md)
