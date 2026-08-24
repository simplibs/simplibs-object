# 🧱 `Copyable` — copy / deepcopy Support

`Copyable` implements Python's standard `copy.copy()` / `copy.deepcopy()` protocol for
Simple instances, built entirely on the shared snapshot foundation.

```python
import copy as _copy
from ...core_mixins import NodesDicts, Snapshot
from ..._commons.immutability import create_new_instance

class Copyable(NodesDicts, Snapshot):
    ...
```

---

## 🧭 Table of Contents

* [`__copy__`](#__copy__)
* [`__deepcopy__`](#__deepcopy__)

---

### `__copy__`

Creates a shallow copy of the instance via a snapshot.

**Parameters:**
* *(none)*

**Returns:**
* a new instance with the same state.

**Example usage:**
```python
import copy
new_obj = copy.copy(obj)
```

**Under the hood:**
```python
def __copy__(self):
    snapshot = self._build_snapshot()
    return create_new_instance(self, snapshot)
```

[▲ Back to top](#-table-of-contents)

---

### `__deepcopy__`

Creates a deep copy of the instance, running every snapshot value through
`copy.deepcopy` with the standard `memo` dict to handle shared references and cycles.

**Parameters:**
* `memo` (*dict[int, Any]*): the `copy` module's memo dict.

**Returns:**
* a new instance with a fully deep-copied state.

**Example usage:**
```python
import copy
new_obj = copy.deepcopy(obj)
```

**Under the hood:**
```python
def __deepcopy__(self, memo):
    snapshot = tuple(_copy.deepcopy(v, memo) for v in self._build_snapshot())
    return create_new_instance(self, snapshot)
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../../README_MIXINS_OVERVIEW.md)
