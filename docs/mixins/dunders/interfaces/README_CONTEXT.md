# 🧱 `ContextManager` — Inert Context Manager Support

`ContextManager` lets a Simple instance be used in a `with obj:` block. It performs no
side effects — no cleanup, no state change — it simply enables the syntax and never
suppresses exceptions.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin

class ContextManager(SimpleMixin):
    ...
```

---

## 🧭 Table of Contents

* [`__enter__`](#__enter__)
* [`__exit__`](#__exit__)

---

### `__enter__`

Returns the instance itself, enabling `with obj as x:` to bind `x` to the same
instance.

**Parameters:**
* *(none)*

**Returns:**
* the instance itself.

**Example usage:**
```python
with obj as x:
    x.do_something()
```

**Under the hood:**
```python
def __enter__(self):
    return self
```

[▲ Back to top](#-table-of-contents)

---

### `__exit__`

Always returns `False`, so any exception raised inside the `with` block propagates
normally.

**Parameters:**
* `exc_type` (*type[BaseException] | None*)
* `exc_val` (*BaseException | None*)
* `exc_tb` (*TracebackType | None*)

**Returns:**
* `Literal[False]`

**Example usage:**
```python
with obj:
    raise ValueError("still propagates")
```

**Under the hood:**
```python
def __exit__(self, exc_type, exc_val, exc_tb):
    return False
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../../README_MIXINS_OVERVIEW.md)
