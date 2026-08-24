# 🧱 `ImmutableWithInners` — Per-Inner Generated Setters

`ImmutableWithInners` generates a dedicated `with_<name>(value)` method for every
inner of a composite, so instead of writing `obj.with_composite("uzel", value)`
generically, callers get a specific, autocomplete-friendly `obj.with_uzel(value)`.

```python
from .ImmutableMethods import ImmutableMethods

class ImmutableWithInners(ImmutableMethods):
    ...
```

`_immutable_only = True`, `_composite_only = True`.

---

## 🧭 Table of Contents

* [`__extend_instance_class__`](#__extend_instance_class__)

---

### `__extend_instance_class__`

Class-creation-time hook. For every inner name in the blueprint, dynamically defines
and attaches a `with_<name>(value)` method that forwards to `with_composite`.

**Parameters:**
* `instance_cls` (*SimpleInstanceLike*): the instance class being built.

**Returns:**
* `SimpleInstanceLike`: the modified class.

**Example usage:**
```python
class Node(ImmutableWithInners, SimpleObject):
    uzel: int

node.with_uzel(5)  # generated automatically
```

**Under the hood:**
```python
@staticmethod
def __extend_instance_class__(instance_cls):
    for name in instance_cls.meta.node_names_set:

        def method(self, value, _name=name):
            return self.with_composite(_name, value)

        method_name = f"with_{name}"
        method.__name__ = method_name
        setattr(instance_cls, method_name, method)

    return instance_cls
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../../README_MIXINS_OVERVIEW.md)
