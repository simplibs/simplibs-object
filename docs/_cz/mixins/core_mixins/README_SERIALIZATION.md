# 🧱 `Serialization` — Universal Import/Export API

`Serialization` is the universal, "master" import/export mixin — `to_dict()` /
`to_json()` for reading an instance out as plain data, and `from_dict()` /
`from_json()` / `update_constants()` for rebuilding or updating one from plain data. It
automatically respects mutable-vs-immutable mode without branching itself.

```python
import json
from .Infrastructure import Infrastructure
from ._utils.serialization import to_dict, from_dict, from_dict_constants

class Serialization(Infrastructure):
    ...
```

---

## 🧭 Table of Contents

* [`to_dict`](#to_dict)
* [`to_json`](#to_json)
* [`from_dict`](#from_dict)
* [`from_json`](#from_json)
* [`update_constants`](#update_constants)

---

### `to_dict`

Serializes the instance into a readable flat dict.

**Parameters:**
* `constant_only` (*bool*, keyword-only, default `False`): if `True`, only constants
  (atoms) are included.

**Returns:**
* `StateDict`: a flat dict representation of the instance.

**Example usage:**
```python
data = person.to_dict()
# {"first_name": "Alice", "last_name": "Smith"}
```

**Under the hood:**
```python
def to_dict(self, *, constant_only: bool = False) -> dict:
    return to_dict(self, constant_only=constant_only)
```

[▲ Back to top](#-table-of-contents)

---

### `to_json`

Serializes the instance into a JSON string, via `to_dict()`.

**Parameters:**
* `**kwargs`: forwarded to `json.dumps`.

**Returns:**
* `str`: JSON representation of the instance.

**Example usage:**
```python
json_str = person.to_json(indent=2)
```

**Under the hood:**
```python
def to_json(self, **kwargs) -> str:
    return json.dumps(self.to_dict(), ensure_ascii=False, **kwargs)
```

[▲ Back to top](#-table-of-contents)

---

### `from_dict`

Reconstructs the instance's state from a dict. Mutable instances are updated in place;
immutable instances return a new instance.

**Parameters:**
* `user_dict` (*StateDict*): the dict to reconstruct from.

**Returns:**
* `SerializationProtocol`: `self` (mutable) or a new instance (immutable).

**Example usage:**
```python
person = person.from_dict({"first_name": "Bob"})
```

**Under the hood:**
```python
def from_dict(self, user_dict: dict) -> "Serialization":
    return from_dict(self, user_dict)
```

[▲ Back to top](#-table-of-contents)

---

### `from_json`

Reconstructs the instance's state from a JSON string, via `from_dict()`.

**Parameters:**
* `json_str` (*str*): the JSON string to reconstruct from.

**Returns:**
* `SerializationProtocol`: `self` (mutable) or a new instance (immutable).

**Example usage:**
```python
person = person.from_json('{"first_name": "Bob"}')
```

**Under the hood:**
```python
def from_json(self, json_str: str) -> "Serialization":
    return self.from_dict(json.loads(json_str))
```

[▲ Back to top](#-table-of-contents)

---

### `update_constants`

Updates only the constants (atoms) from a possibly partial dict.

**Parameters:**
* `user_dict` (*StateDict*): a partial dict containing only constant fields to update.

**Returns:**
* `SerializationProtocol`: `self` (mutable) or a new instance (immutable).

**Example usage:**
```python
person = person.update_constants({"first_name": "Bob"})
```

**Under the hood:**
```python
def update_constants(self, user_dict: dict) -> "Serialization":
    return from_dict_constants(self, user_dict)
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../README_MIXINS_OVERVIEW.md)
