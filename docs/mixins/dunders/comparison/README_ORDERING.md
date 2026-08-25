# 🧱 `Ordering` — Magnitude Comparison

`Ordering` adds `<`, `<=`, `>`, `>=` to a Simple instance, so instances can be sorted,
compared, and used with `min()`/`max()` the same way as the raw values they wrap.
Comparing against an incompatible type returns `NotImplemented` rather than raising.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin

class Ordering(SimpleMixin):
    ...
```

---

## 🧭 Table of Contents

* [`__lt__`](#__lt__)
* [`__le__`](#__le__)
* [`__gt__`](#__gt__)
* [`__ge__`](#__ge__)

[⬅️ Back to main Mixins Overview](../../README_MIXINS_OVERVIEW.md)

---

### `__lt__`

Returns `True` if this instance's value is less than the other operand's value.

**Parameters:**
* `other` (*Any*): a Simple instance or raw value.

**Returns:**
* `bool` or `NotImplemented`

**Example usage:**
```python
age < 30
age < other_age_obj
```

**Under the hood:**
```python
def __lt__(self, other):
    other_value = getattr(other, "value", other)
    try:
        return self.value < other_value
    except TypeError:
        return NotImplemented
```

[▲ Back to top](#-table-of-contents)

---

### `__le__`

Returns `True` if this instance's value is less than or equal to the other operand's
value. Same shape as `__lt__`, using `<=`.

**Parameters:**
* `other` (*Any*)

**Returns:**
* `bool` or `NotImplemented`

**Example usage:**
```python
age <= 30
```

**Under the hood:**
```python
def __le__(self, other):
    other_value = getattr(other, "value", other)
    try:
        return self.value <= other_value
    except TypeError:
        return NotImplemented
```

[▲ Back to top](#-table-of-contents)

---

### `__gt__`

Returns `True` if this instance's value is greater than the other operand's value.
Same shape as `__lt__`, using `>`.

**Parameters:**
* `other` (*Any*)

**Returns:**
* `bool` or `NotImplemented`

**Example usage:**
```python
age > 18
```

**Under the hood:**
```python
def __gt__(self, other):
    other_value = getattr(other, "value", other)
    try:
        return self.value > other_value
    except TypeError:
        return NotImplemented
```

[▲ Back to top](#-table-of-contents)

---

### `__ge__`

Returns `True` if this instance's value is greater than or equal to the other
operand's value. Same shape as `__lt__`, using `>=`.

**Parameters:**
* `other` (*Any*)

**Returns:**
* `bool` or `NotImplemented`

**Example usage:**
```python
age >= 18
```

**Under the hood:**
```python
def __ge__(self, other):
    other_value = getattr(other, "value", other)
    try:
        return self.value >= other_value
    except TypeError:
        return NotImplemented
```

[▲ Back to top](#-table-of-contents)

---

