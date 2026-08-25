# 🧱 `ValueFormatting` — Value-Driven Formatting & Conversion

`ValueFormatting` adds value-driven formatting and conversion — `format()`, f-string
support via `__format__`, `bytes(obj)`, and `bool(obj)` — all routed through
`self.value`, without touching `__repr__`/`__str__`.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin

class ValueFormatting(SimpleMixin):
    ...
```

---

## 🧭 Table of Contents

* [`format`](#format)
* [`__format__`](#__format__)
* [`__bytes__`](#__bytes__)
* [`__bool__`](#__bool__)

[⬅️ Back to main Mixins Overview](../../README_MIXINS_OVERVIEW.md)

---

### `format`

Formats the instance's value according to a pattern, or `meta.mask` if none is given.

**Parameters:**
* `pattern` (*str | None*, default `None`): a format pattern (e.g. `"{:.2f}"`-style).

**Returns:**
* `str`

**Example usage:**
```python
price.format("{:.2f}")
```

**Under the hood:**
```python
def format(self, pattern=None) -> str:
    value = self.value
    mask = pattern or getattr(self.meta, "mask", None)
    if mask and isinstance(value, (str, int, float)):
        return mask.format(value)
    return str(value)
```

[▲ Back to top](#-table-of-contents)

---

### `__format__`

Adapter so f-strings work: `f"{obj:pattern}"`.

**Parameters:**
* `format_spec` (*str*, default `""`)

**Returns:**
* `str`

**Example usage:**
```python
f"{price:{'{:.2f}'}}"
```

**Under the hood:**
```python
def __format__(self, format_spec=""):
    return self.format(format_spec or None)
```

[▲ Back to top](#-table-of-contents)

---

### `__bytes__`

Converts the instance's value to `bytes`. Handles `bytes`, `bytearray`/`memoryview`,
and `str` (UTF-8); raises `TypeError` otherwise.

**Parameters:**
* *(none)*

**Returns:**
* `bytes`

**Example usage:**
```python
bytes(name_obj)
```

**Under the hood:**
```python
def __bytes__(self) -> bytes:
    value = self.value
    if isinstance(value, bytes):
        return value
    if isinstance(value, (bytearray, memoryview)):
        return bytes(value)
    if isinstance(value, str):
        return value.encode("utf-8")
    raise TypeError(f"Cannot convert {self.meta.class_name} to bytes.")
```

[▲ Back to top](#-table-of-contents)

---

### `__bool__`

The object's truthiness matches the truthiness of its value.

**Parameters:**
* *(none)*

**Returns:**
* `bool`

**Example usage:**
```python
if price:
    ...
```

**Under the hood:**
```python
def __bool__(self) -> bool:
    return bool(self.value)
```

[▲ Back to top](#-table-of-contents)

---
