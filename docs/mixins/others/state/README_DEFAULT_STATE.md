# 🧱 `DefaultState` — Construction-Time State Memory

`DefaultState` remembers the state a mutable instance was created with, and provides
three ways to use that memory: reset to it, build a fresh instance from it, or clone
the current state into a new instance.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin
from src.simplibs.object.mixins.core_mixins import Snapshot, NodesTuple

class DefaultState(Snapshot, NodesTuple, SimpleMixin):
    ...
```

`_mutable_only = True`.

---

## 🧭 Table of Contents

* [`init_mixins`](#init_mixins)
* [`clone_instance`](#clone_instance)
* [`reset_to_default_values`](#reset_to_default_values)
* [`create_new_default_instance`](#create_new_default_instance)

---

### `init_mixins`

Captures the default-state snapshot once, right after construction.

**Parameters:**
* *(none)*

**Returns:**
* `None`

**Under the hood:**
```python
def init_mixins(self):
    self._default_state_snapshot = self._build_snapshot()
```

[▲ Back to top](#-table-of-contents)

---

### `clone_instance`

Creates a new instance with the same state as this instance right now.

**Parameters:**
* *(none)*

**Returns:**
* a new instance matching the current state.

**Example usage:**
```python
clone = person.clone_instance()
```

**Under the hood:**
```python
def clone_instance(self):
    new_instance = self.create_new_default_instance()
    new_instance.reset_to_default_values()
    return new_instance
```

[▲ Back to top](#-table-of-contents)

---

### `reset_to_default_values`

Resets the instance back to the state it had at construction time.

**Parameters:**
* *(none)*

**Returns:**
* `None`

**Example usage:**
```python
person.reset_to_default_values()
```

**Under the hood:**
```python
def reset_to_default_values(self):
    self._restore_snapshot(self._default_state_snapshot)
```

[▲ Back to top](#-table-of-contents)

---

### `create_new_default_instance`

Returns a brand-new instance of the same type, seeded with this instance's original
construction-time state.

**Parameters:**
* *(none)*

**Returns:**
* a new instance reflecting the original default state.

**Example usage:**
```python
fresh = person.create_new_default_instance()
```

**Under the hood:**
```python
def create_new_default_instance(self):
    
    # 1. Create a new instance
    new_instance = object.__new__(type(self))
    new_instance.__init__()

    # 2. Load snapshot values
    new_instance.reset_to_default_values()

    # 3. Return the new instance
    return new_instance
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../../README_MIXINS_OVERVIEW.md)
