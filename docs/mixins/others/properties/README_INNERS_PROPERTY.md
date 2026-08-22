# 🧱 `InnersProperty` — Direct-Access Inner Properties

`InnersProperty` dynamically extends composite instances with properties for direct,
convenient access to their inner elements, based on the blueprint definition — the
attribute-style counterpart to `Mapping`'s dict-style access.

```python
from ...base_class import SimpleMixin
from ._utils._utils_for_inners_property import collect_all_nested_properties

class InnersProperty(SimpleMixin):
    ...
```

`_composite_only = True`.

---

## 🧭 Table of Contents

* [`__extend_instance_class__`](#__extend_instance_class__)

---

### `__extend_instance_class__`

Class-creation-time hook. Collects all nested properties for the blueprint and
attaches them to the class.

**Parameters:**
* `instance_cls` (*SimpleInstanceLike*): the instance class being built.

**Returns:**
* `SimpleInstanceLike`: the modified class.

**Example usage:**
```python
class Person(InnersProperty, SimpleObject):
    first_name: str
    last_name: str

person.first_name  # "Alice" — direct property access
```

**Under the hood:**
```python
@staticmethod
def __extend_instance_class__(instance_cls):
    nested_props = collect_all_nested_properties(instance_cls.meta)
    for name, prop in nested_props.items():
        setattr(instance_cls, name, prop)
    return instance_cls
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../../README_MIXINS_OVERVIEW.md)
