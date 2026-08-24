# 🧱 `NodesTuple` — Flattened Node Source of Truth

`NodesTuple` builds the single source of truth for "everything reachable inside this
instance" — a flat, ordered tuple of every node (atom or composite, however deeply
nested) paired with its access path. Every other tree-walking mixin (`NodesDicts`,
`Snapshot`, `Equalizer`, `History`, ...) is ultimately built on top of `_nodes_tuple`.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin

class NodesTuple(SimpleMixin):
    ...
```

---

## 🧭 Table of Contents

* [`init_mixins`](#init_mixins)

---

### `init_mixins`

Builds three derived structures from the instance's node tree, in order: the flat
node tuple itself, a matching tuple of names, and a set of constant names.

**Parameters:**
* *(none — takes only `self`)*

**Returns:**
* `None`

**Example usage:**
```python
# Called implicitly when the instance is constructed
instance = MyComposite(...)
print(instance._nodes_tuple)       # ((atom1, path1), (atom2, path2), ...)
print(instance._node_names_tuple)  # ("first_name", "last_name", ...)
```

**Under the hood:**
```python
def init_mixins(self) -> None:

    self._nodes_tuple = build_nodes_tuple(self)

    self._node_names_tuple = tuple(
        instance.meta.name_snake
        for instance, _ in self._nodes_tuple
    )

    self._constant_names_tuple = {
        instance.meta.name_snake
        for instance, path in self._nodes_tuple
        if path[-1] is not "_value"
    }
```

```python
def build_nodes_tuple(self):

    # 1. Prepare accumulator
    nodes_list = []

    # 2. Recursively collect all nodes
    _collect_nodes_data(
        instance=self,
        path=(),
        nodes_list=nodes_list,
    )

    # 3. Convert to tuple and return
    return tuple(nodes_list)
```

```python
def _collect_nodes_data(instance, path, nodes_list):

    # 1. Add current node (constant)
    if instance.meta.is_constant:
        nodes_list.append((instance, path))
        return

    # 2. Add current node (composite)
    else:
        nodes_list.append((instance, path + ("_value",)))

    # 3. Process composite inners
    for inner in instance.meta.inners:

        # 3.1 Extract metadata
        inner_meta = inner.meta

        # 3.2 Load inner instance
        inner_instance = getattr(instance, inner_meta.name_private)

        # 3.3 Recursive descent
        _collect_nodes_data(
            instance=inner_instance,
            path=path + (inner_meta.name_snake,),
            nodes_list=nodes_list,
        )
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../README_MIXINS_OVERVIEW.md)
