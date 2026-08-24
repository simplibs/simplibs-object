# 🧱 `Call` — Callable Syntax for Value Changes

`Call` lets a Simple instance be called like a function — `obj("a", 10)` — as a
compact shortcut for producing a changed instance. It's syntactic sugar over the
`with_any` change engine; all real logic lives there.

```python
from ..._commons.immutability import with_any
from ...core_mixins import Infrastructure

class Call(Infrastructure):
    ...
```

---

## 🧭 Table of Contents

* [`__call__`](#__call__)

---

### `__call__`

Normalizes the call's argument shape (keyword args → tuple pairs, a single passed-in
tuple unwrapped) and delegates to `with_any`.

**Parameters:**
* `*changes` (*Any*): positional change arguments, e.g. `("a", 10)` pairs.
* `**kwargs` (*Any*): keyword-style changes, e.g. `a=10`.

**Returns:**
* a new (or the same, if mutable) instance reflecting the requested changes.

**Example usage:**
```python
obj("a", 10)
obj(("a", 10), ("b", 20))
obj(a=10, b=20)
```

**Under the hood:**
```python
def __call__(self, *changes, **kwargs):
    if kwargs:
        changes = tuple(kwargs.items())
    elif len(changes) == 1 and isinstance(changes[0], tuple):
        changes = changes[0]
    return with_any(self, changes)
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../../README_MIXINS_OVERVIEW.md)
