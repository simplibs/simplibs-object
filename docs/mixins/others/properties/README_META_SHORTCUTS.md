# 🧱 `MetaShortcuts` — Ergonomic Metadata Shortcuts

`MetaShortcuts` pulls a handful of frequently-needed facts out of `self.meta` and
exposes them as top-level properties on the instance — adds no new behavior, only
convenience.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin

class MetaShortcuts(SimpleMixin):
    ...
```

---

## 🧭 Table of Contents

* [`name_snake`](#name_snake)
* [`value_type`](#value_type)
* [`default`](#default)
* [`is_atom`](#is_atom)
* [`is_composite`](#is_composite)
* [`is_decomposeable`](#is_decomposeable)

[⬅️ Back to main Mixins Overview](../../README_MIXINS_OVERVIEW.md)

---

### `name_snake`

**Returns:** `str` — snake_case name of the object's class.

**Example usage:**
```python
person.name_snake  # "person"
```

**Under the hood:**
```python
@property
def name_snake(self) -> str:
    return self.meta.name_snake
```

[▲ Back to top](#-table-of-contents)

---

### `value_type`

**Returns:** `ValidTypes` — the Python type of the value the object holds.

**Example usage:**
```python
age.value_type  # int
```

**Under the hood:**
```python
@property
def value_type(self):
    return self.meta.value_type
```

[▲ Back to top](#-table-of-contents)

---

### `default`

**Returns:** `Any` — the object's default value, from its metadata.

**Example usage:**
```python
age.default  # 0
```

**Under the hood:**
```python
@property
def default(self):
    return self.meta.default
```

[▲ Back to top](#-table-of-contents)

---

### `is_atom`

**Returns:** `bool` — `True` if the object represents an atom (no inners).

**Example usage:**
```python
age.is_atom  # True
```

**Under the hood:**
```python
@property
def is_atom(self) -> bool:
    return self.meta.is_constant
```

[▲ Back to top](#-table-of-contents)

---

### `is_composite`

**Returns:** `bool` — `True` if the object represents a composite (has inners).
Computed as the negation of `is_atom` to keep a single source of truth.

**Example usage:**
```python
person.is_composite  # True
```

**Under the hood:**
```python
@property
def is_composite(self) -> bool:
    return not self.meta.is_constant
```

[▲ Back to top](#-table-of-contents)

---

### `is_decomposeable`

**Returns:** `bool` — `True` if the object's value can be changed via decomposition.
Uses `getattr(..., False)` to tolerate metadata that doesn't define this field.

**Example usage:**
```python
address.is_decomposeable
```

**Under the hood:**
```python
@property
def is_decomposeable(self) -> bool:
    return getattr(self.meta, "is_decomposeable", False)
```

[▲ Back to top](#-table-of-contents)

---
