# 🧱 `ImmutableMethods` — Core Immutable Change API

`ImmutableMethods` is the core "change without mutating" API for immutable
instances — every method here returns a **new** instance rather than modifying
`self`.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin
from src.simplibs.object.mixins.core_mixins import Snapshot, NodesDicts, NodesTuple

class ImmutableMethods(Snapshot, NodesDicts, NodesTuple, SimpleMixin):
    ...
```

`_immutable_only = True`.

---

## 🧭 Table of Contents

* [`with_constant`](#with_constant)
* [`with_constants`](#with_constants)
* [`with_composite`](#with_composite)
* [`with_changes`](#with_changes)
* [`with_value`](#with_value)
* [`duplicate`](#duplicate)

[⬅️ Back to main Mixins Overview](../../README_MIXINS_OVERVIEW.md)

---

### `with_constant`

Creates a new instance by changing a single constant.

**Parameters:**
* `name` (*str*): the constant's name.
* `new_value` (*Any*): the new value.

**Returns:**
* a new instance.

**Example usage:**
```python
person.with_constant("first_name", "Bob")
```

**Under the hood:**
```python
def with_constant(self, name, new_value):
    return with_constant(self, name, new_value)
```

More info about the with_constant process:  
➡️ [README_WITH_CONSTANT](immutable_logic/README_WITH_CONSTANT.md)  

[▲ Back to top](#-table-of-contents)


---

### `with_constants`

Creates a new instance based on multiple changes at once.

**Parameters:**
* `changes_tuple` (*ChangesTuple | None*, default `None`): tuple of `(name, value)`
  pairs.

**Returns:**
* a new instance.

**Example usage:**
```python
person.with_constants((("first_name", "Bob"), ("last_name", "Jones")))
```

**Under the hood:**
```python
def with_constants(self, changes_tuple=None):
    return with_constants(self, changes_tuple)
```

More info about the with_constants process:  
➡️ [README_WITH_CONSTANTS](immutable_logic/README_WITH_CONSTANTS.md)  

[▲ Back to top](#-table-of-contents)

---

### `with_composite`

Creates a new instance by changing a single composite (or constant — it routes
appropriately).

**Parameters:**
* `name` (*str*): the composite's name.
* `new_value` (*Any*): the new value.

**Returns:**
* a new instance.

**Example usage:**
```python
person.with_composite("address", new_address_obj)
```

**Under the hood:**
```python
def with_composite(self, name, new_value):
    return with_composite(self, name, new_value)
```

More info about the with_composite process:  
➡️ [README_WITH_COMPOSITE](immutable_logic/README_WITH_COMPOSITE.md)  


[▲ Back to top](#-table-of-contents)

---

### `with_changes`

Applies multiple changes given as a dict.

**Parameters:**
* `changes_dict` (*ChangesDict*): a dict of `{name: new_value}`.

**Returns:**
* a new instance.

**Example usage:**
```python
person.with_changes({"first_name": "Bob", "last_name": "Jones"})
```

**Under the hood:**
```python
def with_changes(self, changes_dict):
    if not isinstance(changes_dict, dict):
        raise_with_changes_input_not_dict(self, changes_dict)
    return with_any(self, tuple(changes_dict.items()))
```

More information about the with_any process:  
➡️ [README_WITH_ANY](immutable_logic/README_WITH_ANY.md)  

[▲ Back to top](#-table-of-contents)

---

### `with_value`

Convenience alias for changing the instance's own top-level value.

**Parameters:**
* `new_value` (*Any*): the new value.

**Returns:**
* a new instance.

**Example usage:**
```python
age.with_value(30)
```

**Under the hood:**
```python
def with_value(self, new_value):
    return self.with_composite(self.meta.name_snake, new_value)
```

[▲ Back to top](#-table-of-contents)

---

### `duplicate`

Returns a new instance with the same values as this one — no changes applied.

**Parameters:**
* *(none)*

**Returns:**
* a new, equal-but-distinct instance.

**Example usage:**
```python
copy_of_person = person.duplicate()
```

**Under the hood:**
```python
def duplicate(self):
    return create_new_instance(self, self._build_snapshot())
```

More information about create_new_instance can be found here:  
➡️ [README_WITH_CONSTANT](immutable_logic/README_WITH_CONSTANT.md)  

[▲ Back to top](#-table-of-contents)

---

