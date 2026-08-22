# 🧱 `NodesTuple` — Flattened Node Source of Truth

`NodesTuple` builds the single source of truth for "everything reachable inside this
instance" — a flat, ordered tuple of every node (atom or composite, however deeply
nested) paired with its access path. Every other tree-walking mixin (`NodesDicts`,
`Snapshot`, `Equalizer`, `History`, ...) is ultimately built on top of `_nodes_tuple`.

```python
from ..base_class import SimpleMixin
from .._commons.constants import VALUE
from ._utils.nodes_tuple import build_nodes_tuple

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
    super().init_mixins()

    self._nodes_tuple = build_nodes_tuple(self)

    self._node_names_tuple = tuple(
        instance.meta.name_snake
        for instance, _ in self._nodes_tuple
    )

    self._constant_names_tuple = {
        instance.meta.name_snake
        for instance, path in self._nodes_tuple
        if path[-1] is not VALUE
    }
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../README_MIXINS_OVERVIEW.md)
