# 🧱 `ClassGetItem` — Generic Subscript Syntax

`ClassGetItem` lets a Simple class be subscripted like `MyClass[int]` without having
to inherit from `typing.Generic`. Purely cosmetic/typing sugar — it doesn't change
what the class does at runtime.

```python
from ...base_class import SimpleMixin

class ClassGetItem(SimpleMixin):
    ...
```

---

## 🧭 Table of Contents

* [`__class_getitem__`](#__class_getitem__)

---

### `__class_getitem__`

Looks up `__class_getitem__` on the parent class; if the parent defines one, defers
to it, otherwise falls back to returning the class itself unchanged.

**Parameters:**
* `item` (*Any*): the subscript argument, e.g. `int` in `MyClass[int]`.

**Returns:**
* `type[Self] | Any`: the parent's result, or the class itself.

**Example usage:**
```python
MyClass[int]  # returns MyClass, or delegates to a Generic parent
```

**Under the hood:**
```python
@classmethod
def __class_getitem__(cls, item):
    super_cls = super(ClassGetItem, cls)
    method = getattr(super_cls, "__class_getitem__", None)
    return method(item) if method is not None else cls
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../../README_MIXINS_OVERVIEW.md)
