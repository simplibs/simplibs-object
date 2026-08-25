# 🧱 `Lifecycle` — Combined Copy + Pickle Bundle

`Lifecycle` is a convenience bundle mixin combining `Copyable` and `PicleReduce`, so
an instance gets full `copy`/`deepcopy`/`pickle` support from a single mixin.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin
from src.simplibs.object.mixins.core_mixins import NodesDicts, NodesTuple, Snapshot
from ..PickleState import PickleState
from ..PickleReduce import PicleReduce
from ..Copyable import Copyable

class Lifecycle(PickleState, PicleReduce, Copyable, Snapshot, NodesDicts, NodesTuple, SimpleMixin):
    ...
```

---

## 🧭 Table of Contents

* [Composition](#composition)

[⬅️ Back to main Mixins Overview](../../../README_MIXINS_OVERVIEW.md)

---

### Composition

`Lifecycle` declares no methods and no slots of its own.

**Provides (via `Copyable`):**
* `__copy__`, `__deepcopy__`

**Provides (via `PicleReduce` → `PickleState`):**
* `__reduce__`, `__getstate__`, `__setstate__`

**Example usage:**
```python
import copy, pickle

new_obj = copy.deepcopy(obj)
data = pickle.dumps(obj)
```

**Under the hood:**
```python
class Lifecycle(Copyable, PicleReduce):
    __slots__ = ()
```

[▲ Back to top](#-table-of-contents)

---

