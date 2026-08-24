# 🧱 `Snapshot` — Build, Restore & Compare Instance State

`Snapshot` gives an instance the ability to capture its entire state as a plain, inert
tuple of values, and later restore or compare against that captured state. This is the
shared foundation behind copying, pickling, default-state resets, dirty tracking, and
undo/redo history.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin
from .NodesTuple import NodesTuple

class Snapshot(NodesTuple, SimpleMixin):
    ...
```

---

## 🧭 Table of Contents

* [`_build_snapshot`](#_build_snapshot)
* [`_restore_snapshot`](#_restore_snapshot)
* [`_compare_snapshots`](#_compare_snapshots)

---

### `_build_snapshot`

Captures the current value of every node in the instance's tree, in the fixed order
defined by `_nodes_tuple`.

**Parameters:**
* *(none — takes only `self`)*

**Returns:**
* `SnapshotTuple`: a plain tuple of raw values, position-matched to `_nodes_tuple`.

**Example usage:**
```python
snapshot = instance._build_snapshot()
# (10, "Alice", True, ...)
```

**Under the hood:**
```python
def _build_snapshot(self) -> tuple:
    return tuple(
        instance._value for instance, _
        in self._nodes_tuple
    )
```

[▲ Back to top](#-table-of-contents)

---

### `_restore_snapshot`

Writes a previously captured snapshot back onto the instance's nodes, bypassing the
normal setter/validation pipeline.

**Parameters:**
* `snapshot` (*SnapshotTuple*): a tuple of values, in the same order as `_nodes_tuple`.

**Returns:**
* `None`

**Example usage:**
```python
old_snapshot = instance._build_snapshot()
instance.value = 99
instance._restore_snapshot(old_snapshot)  # back to how it was
```

**Under the hood:**
```python
def _restore_snapshot(self, snapshot: tuple) -> None:
    for (instance, _), value in zip(self._nodes_tuple, snapshot):
        instance._value = value
```

[▲ Back to top](#-table-of-contents)

---

### `_compare_snapshots`

Compares two snapshots and translates the positional differences back into meaningful
`(path, old_value, new_value)` triples.

**Parameters:**
* `snapshot1` (*SnapshotTuple*): the earlier snapshot.
* `snapshot2` (*SnapshotTuple*): the later snapshot.
* `constants_only` (*bool*, keyword-only, default `False`): if `True`, only differences
  in leaf constants are reported, ignoring composite-level "value" nodes.

**Returns:**
* `SnapshotDiffTuple`: a tuple of changed `(path, old_value, new_value)` entries.

**Example usage:**
```python
diff = instance._compare_snapshots(old_snapshot, new_snapshot, constants_only=True)
```

**Under the hood:**
```python
def _compare_snapshots(self, snapshot1, snapshot2, *, constants_only=False):
    diffs = []
    nodes_tuple = self._nodes_tuple

    try:
        # 1. Iterate through nodes and both snapshots simultaneously
        for (_, path), snap1_value, snap2_value in zip(nodes_tuple, snapshot1, snapshot2):

            # 2. Skip composite nodes when constants_only=True
            if constants_only and path[-1] == "_value":
                continue

            # 3. Append differences
            if snap1_value != snap2_value:
                diffs.append((path, snap1_value, snap2_value))

        return tuple(diffs)

    except (ValueError, TypeError) as error:
        raise_snapshot_incompatible_error(
            nodes_tuple=nodes_tuple,
            snapshot1=snapshot1,
            snapshot2=snapshot2,
            error=error,
        )
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../README_MIXINS_OVERVIEW.md)
