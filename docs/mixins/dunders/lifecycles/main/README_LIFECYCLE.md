# 🧱 `Lifecycle` — Combined Copy + Pickle Bundle

`Lifecycle` is a convenience bundle mixin combining `Copyable` and `PicleReduce`, so
an instance gets full `copy`/`deepcopy`/`pickle` support from a single mixin.

```python
from ..PickleReduce import PicleReduce
from ..Copyable import Copyable

class Lifecycle(Copyable, PicleReduce):
    ...
```

---

## 🧭 Table of Contents

* [Composition](#composition)

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

[⬅️ Back to Mixins Overview](../../../../README_MIXINS_OVERVIEW.md)
