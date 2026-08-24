# 🧱 `DirtyTracking` — Snapshot-Based Change Detection

`DirtyTracking` tracks whether a mutable instance has changed since a reference
point — `is_dirty`, `dirty_paths`, `reset_to_clean()`, `mark_clean()` — the same
concept as "unsaved changes" indicators in editors, generalized to nested composites.

```python
from ...core_mixins import Snapshot

class DirtyTracking(Snapshot):
    ...
```

`_mutable_only = True`.

---

## 🧭 Table of Contents

* [`init_mixins`](#init_mixins)
* [`is_dirty`](#is_dirty)
* [`dirty_paths`](#dirty_paths)
* [`clean_snapshot`](#clean_snapshot)
* [`get_dirty_paths`](#get_dirty_paths)
* [`reset_to_clean`](#reset_to_clean)
* [`mark_clean`](#mark_clean)

---

### `init_mixins`

Captures the initial clean snapshot right after construction.

**Parameters:**
* *(none)*

**Returns:**
* `None`

**Under the hood:**
```python
def init_mixins(self):
    super().init_mixins()
    self._clean_snapshot = self._build_snapshot()
```

[▲ Back to top](#-table-of-contents)

---

### `is_dirty`

`True` if the current state differs from the clean snapshot.

**Parameters:**
* *(none — property getter)*

**Returns:**
* `bool`

**Example usage:**
```python
person.first_name = "Bob"
person.is_dirty  # True
```

**Under the hood:**
```python
@property
def is_dirty(self) -> bool:
    current_snapshot = self._build_snapshot()
    return current_snapshot != self._clean_snapshot
```

[▲ Back to top](#-table-of-contents)

---

### `dirty_paths`

Returns the changed constant paths as `(path, old_value, new_value)` triples.

**Parameters:**
* *(none — property getter)*

**Returns:**
* `SnapshotDiffTuple`

**Example usage:**
```python
person.dirty_paths
```

**Under the hood:**
```python
@property
def dirty_paths(self):
    current_snapshot = self._build_snapshot()
    return self._compare_snapshots(
        self._clean_snapshot, current_snapshot, constants_only=True
    )
```

[▲ Back to top](#-table-of-contents)

---

### `clean_snapshot`

Returns the stored clean snapshot itself.

**Parameters:**
* *(none — property getter)*

**Returns:**
* `SnapshotTuple`

**Under the hood:**
```python
@property
def clean_snapshot(self):
    return self._clean_snapshot
```

[▲ Back to top](#-table-of-contents)

---

### `get_dirty_paths`

Like `dirty_paths`, but lets the caller include composite-level changes too.

**Parameters:**
* `constants_only` (*bool*, keyword-only, default `True`)

**Returns:**
* `SnapshotDiffTuple`

**Example usage:**
```python
person.get_dirty_paths(constants_only=False)
```

**Under the hood:**
```python
def get_dirty_paths(self, *, constants_only=True):
    return self._compare_snapshots(
        self._clean_snapshot, self._build_snapshot(), constants_only=constants_only
    )
```

[▲ Back to top](#-table-of-contents)

---

### `reset_to_clean`

Restores the object to its clean snapshot, discarding all changes.

**Parameters:**
* *(none)*

**Returns:**
* `None`

**Under the hood:**
```python
def reset_to_clean(self) -> None:
    self._restore_snapshot(self._clean_snapshot)
```

[▲ Back to top](#-table-of-contents)

---

### `mark_clean`

Marks the current state as the new clean snapshot (e.g. after a "save").

**Parameters:**
* *(none)*

**Returns:**
* `None`

**Under the hood:**
```python
def mark_clean(self) -> None:
    self._clean_snapshot = self._build_snapshot()
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../../README_MIXINS_OVERVIEW.md)
