# 🧱 `Permission` — Runtime Read-Only Lock

`Permission` gives a mutable instance a runtime read-only switch — `obj.lock()` turns
further writes into errors, `obj.unlock()` turns them back on. Unlike structural
immutability, this is a *runtime* toggle on an otherwise mutable instance.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin

class Permission(SimpleMixin):
    ...
```

`_mutable_only = True`.

> **Note:** `_locked` itself is not initialized by this mixin. Every atomic instance
> already carries `self._locked = False`, set directly by `create_atom_init`, and the
> enforcement (`if self._locked: raise ...`) lives inside `create_value_setter` — both
> exist specifically to support this mixin, folded into the shared atomic-instance
> construction rather than routed through a separate access path. `Permission` only
> exposes a friendly public API over that existing infrastructure.

---

## 🧭 Table of Contents

* [`is_locked`](#is_locked)
* [`lock`](#lock)
* [`unlock`](#unlock)

[⬅️ Back to main Mixins Overview](../../README_MIXINS_OVERVIEW.md)

---

### `is_locked`

Returns whether the lock is currently active.

**Parameters:**
* *(none — property getter)*

**Returns:**
* `bool`

**Example usage:**
```python
if obj.is_locked:
    print("read-only")
```

**Under the hood:**
```python
@property
def is_locked(self) -> bool:
    return self._locked
```

[▲ Back to top](#-table-of-contents)

---

### `lock`

Engages the lock, making further writes raise an error.

**Parameters:**
* *(none)*

**Returns:**
* `None`

**Example usage:**
```python
obj.lock()
obj.value = 10  # → ValueError
```

**Under the hood:**
```python
def lock(self) -> None:
    object.__setattr__(self, "_locked", True)
```

[▲ Back to top](#-table-of-contents)

---

### `unlock`

Releases the lock, allowing writes again.

**Parameters:**
* *(none)*

**Returns:**
* `None`

**Example usage:**
```python
obj.unlock()
obj.value = 10  # works again
```

**Under the hood:**
```python
def unlock(self) -> None:
    object.__setattr__(self, "_locked", False)
```

[▲ Back to top](#-table-of-contents)

---

