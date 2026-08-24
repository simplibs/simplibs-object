# 🧱 `Mapping` — Dict-Style Item Access for Composites

`Mapping` gives a composite instance `dict`-style item access: `obj[key]`,
`obj[key] = value`, `key in obj`, `obj.get(key, default)`, `len(obj)`.

```python
from .CollectionBase import CollectionBase

class Mapping(CollectionBase):
    ...
```

`_composite_only = True` — item access only makes sense over a composite's inners.

---

## 🧭 Table of Contents

* [`__len__`](#__len__)
* [`__contains__`](#__contains__)
* [`__missing__`](#__missing__)
* [`__getitem__`](#__getitem__)
* [`get`](#get)
* [`__setitem__`](#__setitem__)

---

### `__len__`

Returns the number of direct inners.

**Parameters:**
* *(none)*

**Returns:**
* `int`

**Example usage:**
```python
len(person)  # 2
```

**Under the hood:**
```python
def __len__(self) -> int:
    return len(self._inners_name_tuple)
```

[▲ Back to top](#-table-of-contents)

---

### `__contains__`

Checks whether the composite contains an inner with the given key.

**Parameters:**
* `key` (*str*): the key to check.

**Returns:**
* `bool`

**Example usage:**
```python
"first_name" in person  # True
```

**Under the hood:**
```python
def __contains__(self, key: str) -> bool:
    return key in self._inners_name_set
```

[▲ Back to top](#-table-of-contents)

---

### `__missing__`

Raises `KeyError` with a message listing the available keys. Called by `__getitem__`
when a key is not found.

**Parameters:**
* `key` (*str*): the missing key.

**Returns:**
* `None` (always raises)

**Example usage:**
```python
person["nickname"]  # KeyError: 'nickname' not defined. Available: [...]
```

**Under the hood:**
```python
def __missing__(self, key: str) -> None:
    raise KeyError(
        f"Item '{key}' is not defined on {self.meta.class_name}. "
        f"Available items: {self.keys()}"
    )
```

[▲ Back to top](#-table-of-contents)

---

### `__getitem__`

Returns the value of an inner by key, or raises via `__missing__`.

**Parameters:**
* `key` (*str*): the inner's name.

**Returns:**
* the inner's current value.

**Example usage:**
```python
person["first_name"]  # "Alice"
```

**Under the hood:**
```python
def __getitem__(self, key: str):
    if key not in self._inners_name_set:
        self.__missing__(key)
    return getattr(self, key)
```

[▲ Back to top](#-table-of-contents)

---

### `get`

Safely returns the value of an inner, or a default if the key doesn't exist.

**Parameters:**
* `key` (*str*): the inner's name.
* `default` (*Any*, default `None`): the fallback value.

**Returns:**
* the inner's value, or `default`.

**Example usage:**
```python
person.get("nickname", "N/A")  # "N/A"
```

**Under the hood:**
```python
def get(self, key: str, default=None):
    if key not in self._inners_name_set:
        return default
    return getattr(self, key)
```

[▲ Back to top](#-table-of-contents)

---

### `__setitem__`

Sets the value of an inner by key, if the instance is mutable and the key exists.

**Parameters:**
* `key` (*str*): the inner's name.
* `value` (*Any*): the new value.

**Returns:**
* `None`

**Example usage:**
```python
person["first_name"] = "Bob"
```

**Under the hood:**
```python
def __setitem__(self, key: str, value) -> None:
    if not self.__is_mutable__:
        raise TypeError("Immutable composite does not allow __setitem__.")
    if key not in self._inners_name_set:
        self.__missing__(key)
    setattr(self, key, value)
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../../README_MIXINS_OVERVIEW.md)
