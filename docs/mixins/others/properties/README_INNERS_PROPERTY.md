# 🧱 `InnersProperty` — Direct-Access Inner Properties

`InnersProperty` dynamically extends composite instances with properties for direct,
convenient access to their inner elements, based on the blueprint definition — the
attribute-style counterpart to `Mapping`'s dict-style access.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin

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

```python
def collect_all_nested_properties(meta):

    # 1. Initialize result container
    result = {}

    # 2. Iterate through direct inners
    for inner in meta.inners:

        # 2.1 Extract metadata
        inner_meta = inner.meta
        inner_meta: "SimpleMetadataLike"

        # 2.2 Process only composite inners
        if not inner_meta.is_constant:

            # 2.2.1 Build initial path tuple
            path = (inner_meta.name_private,)

            # 2.2.2 Recursively collect nested properties
            _collect_nested_inner_properties(inner_meta, path, result)

    # 3. Return collected properties
    return result
```

```python
def _collect_nested_inner_properties(meta, path, result):

    # 1. Iterate through inner elements
    for inner in meta.inners:

        # 1.1 Extract metadata and extend path
        inner_meta = inner.meta
        new_path = path + (inner_meta.name_private,)

        # 1.2 Create properties (for constants and composites)
        props = create_properties_for_inner(inner_meta, new_path)
        result.update(props)

        # 1.3 Recursively process composite inners
        if not inner_meta.is_constant:
            _collect_nested_inner_properties(inner_meta, new_path, result)
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../../README_MIXINS_OVERVIEW.md)
