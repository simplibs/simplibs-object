# 🧱 `PicleReduce` — Pickle Protocol Entry Point

`PicleReduce` implements `__reduce__`, the top-level hook `pickle` calls first to
learn how to reconstruct an object: what callable to invoke, what arguments to pass,
and what state to apply afterward. Builds on `PickleState` to reuse its
`__getstate__` implementation.

> Note: the class name keeps the original spelling `PicleReduce` (missing a "k") to
> match the existing codebase.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin
from src.simplibs.object.mixins.core_mixins import NodesDicts, NodesTuple, Snapshot
from .PickleState import PickleState

class PicleReduce(PickleState, Snapshot, NodesDicts, NodesTuple, SimpleMixin):
    ...
```

---

## 🧭 Table of Contents

* [`__reduce__`](#__reduce__)

---

### `__reduce__`

Returns the standard 3-tuple `pickle` expects: the reconstructing callable, its
arguments, and the state to apply.

**Parameters:**
* *(none)*

**Returns:**
* `tuple[type, tuple, StateDict]`

**Example usage:**
```python
import pickle
data = pickle.dumps(obj)
restored = pickle.loads(data)
```

**Under the hood:**
```python
def __reduce__(self):
    return (
        self.__class__,
        (),
        self.__getstate__()
    )
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../../README_MIXINS_OVERVIEW.md)
