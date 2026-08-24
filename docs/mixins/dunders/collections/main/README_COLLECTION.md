# 🧱 `Collection` — Combined Iteration + Mapping Bundle

`Collection` is a convenience bundle mixin combining `Iterable` and `Mapping` into a
single mixin, so a composite instance can behave like a full read-mostly mapping
(iteration, `len()`, `in`, `obj[key]`, `keys()`/`values()`/`items()`) without listing
both mixins separately.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin
from ..Iterable import Iterable
from ..Mapping import Mapping
from ..CollectionBase import CollectionBase

class Collection(Iterable, Mapping, CollectionBase, SimpleMixin):
    ...
```

---

## 🧭 Table of Contents

* [Composition](#composition)

---

### Composition

`Collection` declares no methods and no slots of its own.

**Provides (via `Iterable`):**
* `__iter__`, `__reversed__`, `__dir__`

**Provides (via `Mapping`):**
* `__len__`, `__contains__`, `__getitem__`, `__setitem__`, `get`

**Provides (via shared `CollectionBase`):**
* `keys()`, `values()`, `items()`

**Example usage:**
```python
class Person(Collection, SimpleObject):
    ...

for key in person:
    print(key, person[key])
```

**Under the hood:**
```python
class Collection(Iterable, Mapping):
    _composite_only = True
    __slots__ = ()
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../../../README_MIXINS_OVERVIEW.md)
