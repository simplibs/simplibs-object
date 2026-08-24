# 🧱 `Infrastructure` — Shared Node & Snapshot Foundation

`Infrastructure` is a convenience bundle mixin combining `NodesDicts` and `Snapshot`
into a single shared foundation. It adds no logic of its own — any mixin that needs
both name-keyed node lookup and snapshot-based state (build / restore / compare) can
inherit from this one class instead of listing both parents separately.

```python
from .NodesDicts import NodesDicts
from .Snapshot import Snapshot

class Infrastructure(NodesDicts, Snapshot):
    ...
```

`Infrastructure` is the base class for `Serialization`, `ImmutableMethods`, and every
other mixin that needs to walk or snapshot the instance's node tree.

---

## 🧭 Table of Contents

* [Composition](#composition)

---

### Composition

`Infrastructure` declares no methods and no slots of its own — its entire purpose is
the multiple-inheritance combination.

**Provides (via `NodesDicts`):**
* `_nodes_dict`, `_nodes_instance_dict`, `_nodes_path_dict`, `_nodes_index_map`

**Provides (via `Snapshot`):**
* `_build_snapshot()`, `_restore_snapshot()`, `_compare_snapshots()`

**Example usage:**
```python
class Serialization(Infrastructure):
    def to_dict(self, *, constant_only: bool = False) -> dict:
        return to_dict(self, constant_only=constant_only)
```

**Under the hood:**
```python
class Infrastructure(NodesDicts, Snapshot):
    __slots__ = ()
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../README_MIXINS_OVERVIEW.md)
