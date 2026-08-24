# 🧱 `PickleState` — Pickle State via to_dict / from_dict

`PickleState` bridges `pickle`'s `__getstate__`/`__setstate__` hooks to the
`to_dict()`/`from_dict()` serialization the ecosystem already provides, so pickled
data is a readable dict rather than an opaque attribute dump.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin
from src.simplibs.object.mixins.core_mixins import NodesDicts, NodesTuple, Snapshot

class PickleState(Snapshot, NodesDicts, NodesTuple, SimpleMixin):
    ...
```

Requires the class to provide `from_dict()` (from `MutableSerialization` or
`ImmutableSerialization`) — missing it raises `TypeError`.

---

## 🧭 Table of Contents

* [`__getstate__`](#__getstate__)
* [`__setstate__`](#__setstate__)

---

### `__getstate__`

Returns the instance's state as a dict, via `to_dict()`.

**Parameters:**
* *(none)*

**Returns:**
* `StateDict`

**Example usage:**
```python
import pickle
data = pickle.dumps(obj)  # internally calls __getstate__
```

**Under the hood:**
```python
def __getstate__(self) -> dict:
    return self.to_dict()
```

[▲ Back to top](#-table-of-contents)

---

### `__setstate__`

Restores the instance's state from a dict, via `from_dict()`. Mutable instances are
updated in place; immutable instances are transparently swapped for a new instance by
`pickle`.

**Parameters:**
* `state` (*StateDict*): the dict to restore from.

**Returns:**
* `None`

**Example usage:**
```python
obj = pickle.loads(data)  # internally calls __setstate__
```

**Under the hood:**
```python
def __setstate__(self, state: dict) -> None:
    if not hasattr(self.__class__, "from_dict"):
        raise TypeError(f"{self.__class__.__name__} requires from_dict().")
    self.from_dict(state)
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../../README_MIXINS_OVERVIEW.md)
