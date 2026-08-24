# 🧱 `NodesDicts` — Fast Name-Keyed Node Lookup

`NodesDicts` turns the ordered `_nodes_tuple` from `NodesTuple` into fast, read-only,
name-keyed lookup dictionaries — so instead of scanning the tuple linearly to find a
node by name, mixins can do a direct dict lookup.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin
from .NodesTuple import NodesTuple

class NodesDicts(NodesTuple, SimpleMixin):
    ...
```

---

## 🧭 Table of Contents

* [`init_mixins`](#init_mixins)

---

### `init_mixins`

Builds four `MappingProxyType` (read-only) dicts from `_nodes_tuple`, all keyed by
`instance.meta.name_snake`.

**Parameters:**
* *(none — takes only `self`)*

**Returns:**
* `None`

**Example usage:**
```python
instance = MyComposite(...)
node, path = instance._nodes_dict["first_name"]
inner_instance = instance._nodes_instance_dict["first_name"]
index = instance._nodes_index_map["first_name"]
```

**Under the hood:**
```python
def init_mixins(self) -> None:

    self._nodes_dict = MappingProxyType({
        instance.meta.name_snake: (instance, path)
        for instance, path in self._nodes_tuple
    })

    self._nodes_instance_dict = MappingProxyType({
        instance.meta.name_snake: instance
        for instance, _ in self._nodes_tuple
    })

    self._nodes_path_dict = MappingProxyType({
        instance.meta.name_snake: path
        for instance, path in self._nodes_tuple
    })

    self._nodes_index_map = MappingProxyType({
        instance.meta.name_snake: index
        for index, (instance, _) in enumerate(self._nodes_tuple)
    })
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../README_MIXINS_OVERVIEW.md)
