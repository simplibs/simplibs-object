# 🧱 `Equality` — Value-Based Equality & Hashing

`Equality` gives a Simple instance sensible `==` and `hash()` behavior. Equality
compares values (unwrapping other Simple instances); hashing strategy depends on
mutability — identity hash for mutable instances, value hash for immutable ones.

```python
from ...base_class import SimpleMixin

class Equality(SimpleMixin):
    ...
```

---

## 🧭 Table of Contents

* [`__eq__`](#__eq__)
* [`__hash__`](#__hash__)

---

### `__eq__`

Compares this instance's value against another Simple instance (same blueprint +
value) or a raw value.

**Parameters:**
* `other` (*Any*): the value or instance to compare against.

**Returns:**
* `bool`

**Example usage:**
```python
age == 20            # compares against a raw value
age == other_age_obj  # compares two Simple instances
```

**Under the hood:**
```python
def __eq__(self, other) -> bool:
    if hasattr(other, "meta") and hasattr(other, "value"):
        if self.meta.blueprint_path == other.meta.blueprint_path:
            return self.value == other.value
        return False
    return self.value == other
```

[▲ Back to top](#-table-of-contents)

---

### `__hash__`

Returns identity hash for mutable instances (value may change after hashing), value
hash for immutable instances (value never changes, so it's safe).

**Parameters:**
* *(none)*

**Returns:**
* `int`

**Example usage:**
```python
hash(age)
{age: "twenty"}  # usable as a dict key
```

**Under the hood:**
```python
def __hash__(self) -> int:
    return id(self) if self.__is_mutable__ else hash(self.value)
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../../README_MIXINS_OVERVIEW.md)
