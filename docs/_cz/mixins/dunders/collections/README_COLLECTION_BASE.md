# 🧱 `CollectionBase` — Base Mapping Foundation

`CollectionBase` gives a composite instance basic "mapping" behavior — it starts to
feel a little like a read-only dict. Provides `keys()`, `values()`, `items()` over the
instance's direct inners, and freezes the underlying key structures once at init time.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin

class CollectionBase(SimpleMixin):
    ...
```

`_composite_only = True` — only makes sense for composites; an atomic constant has no
inners to map.

---

## 🧭 Table of Contents

* [`init_mixins`](#init_mixins)
* [`keys`](#keys)
* [`values`](#values)
* [`items`](#items)

---

### `init_mixins`

Freezes two derived structures from the instance's direct inners: an ordered tuple of
keys, and a set of keys for fast membership checks.

**Parameters:**
* *(none — takes only `self`)*

**Returns:**
* `None`

**Example usage:**
```python
person = Person(first_name="Alice", last_name="Smith")
print(person._inners_name_tuple)  # ("first_name", "last_name")
```

**Under the hood:**
```python
def init_mixins(self) -> None:
    super().init_mixins()
    self._inners_name_tuple = tuple(
        inner.meta.name_snake
        for inner in self.meta.inners
    )
    self._inners_name_set = set(self._inners_name_tuple)
```

[▲ Back to top](#-table-of-contents)

---

### `keys`

Returns the keys of all direct inners.

**Parameters:**
* *(none)*

**Returns:**
* `list[str]`: the inner keys, in blueprint-defined order.

**Example usage:**
```python
person.keys()  # ["first_name", "last_name"]
```

**Under the hood:**
```python
def keys(self) -> list[str]:
    return list(self._inners_name_tuple)
```

[▲ Back to top](#-table-of-contents)

---

### `values`

Returns the current value of each direct inner.

**Parameters:**
* *(none)*

**Returns:**
* `list[object]`: values, in the same order as `keys()`.

**Example usage:**
```python
person.values()  # ["Alice", "Smith"]
```

**Under the hood:**
```python
def values(self) -> list:
    return [getattr(self, key) for key in self._inners_name_tuple]
```

[▲ Back to top](#-table-of-contents)

---

### `items`

Returns (key, value) pairs for all direct inners.

**Parameters:**
* *(none)*

**Returns:**
* `list[tuple[str, object]]`

**Example usage:**
```python
person.items()  # [("first_name", "Alice"), ("last_name", "Smith")]
```

**Under the hood:**
```python
def items(self) -> list[tuple]:
    return [(key, getattr(self, key)) for key in self._inners_name_tuple]
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../../README_MIXINS_OVERVIEW.md)
