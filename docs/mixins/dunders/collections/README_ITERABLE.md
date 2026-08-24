# 🧱 `Iterable` — Iteration Support for Composites

`Iterable` makes a composite instance iterable the way Python programmers expect:
`for key in person`, `reversed(person)`, and a `dir(person)` that also shows the inner
names.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin
from .CollectionBase import CollectionBase

class Iterable(CollectionBase, SimpleMixin):
    ...
```

`_composite_only = True` — builds directly on `CollectionBase`'s frozen key tuple.

---

## 🧭 Table of Contents

* [`__iter__`](#__iter__)
* [`__reversed__`](#__reversed__)
* [`__dir__`](#__dir__)

---

### `__iter__`

Iterates over the keys of all inners, in defined order.

**Parameters:**
* *(none)*

**Returns:**
* `Iterator[str]`

**Example usage:**
```python
for key in person:
    print(key)
```

**Under the hood:**
```python
def __iter__(self):
    return iter(self._inners_name_tuple)
```

[▲ Back to top](#-table-of-contents)

---

### `__reversed__`

Returns a reverse iterator over the inner keys.

**Parameters:**
* *(none)*

**Returns:**
* `Iterator[str]`

**Example usage:**
```python
list(reversed(person))  # ["last_name", "first_name"]
```

**Under the hood:**
```python
def __reversed__(self):
    return reversed(self._inners_name_tuple)
```

[▲ Back to top](#-table-of-contents)

---

### `__dir__`

Extends the standard attribute listing with the inner keys, so autocomplete and
`dir()` reveal the composite's structure.

**Parameters:**
* *(none)*

**Returns:**
* `list[str]`

**Example usage:**
```python
dir(person)  # includes "first_name", "last_name", plus normal attributes
```

**Under the hood:**
```python
def __dir__(self):
    base = list(object.__dir__(self))
    base += list(self._inners_name_tuple)
    return sorted(set(base))
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../../README_MIXINS_OVERVIEW.md)
