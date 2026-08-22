# 🧱 `History` — Full Undo/Redo History

`History` provides a full undo/redo history for a mutable instance. State-changing
actions are recorded as timestamped snapshots, navigable step by step or by
index/timestamp, diffable between any two points, and exportable to/from a dict.

```python
from datetime import datetime
from ..core_mixins import Serialization
from ._history_utils.core import set_history_limit, record_state, find_snapshot
from ._history_utils.transfer import export_history_to_dict, import_history_from_dict
from ._history_utils.navigations import (
    history_undo, history_redo,
    go_to_last_history, go_to_history_on_timestamp, go_to_history_on_index
)

class History(Serialization):
    ...
```

`_mutable_only = True`.

---

## 🧭 Table of Contents

* [`init_mixins`](#init_mixins)
* [`record_state`](#record_state)
* [`history`](#history)
* [`history_index`](#history_index)
* [`history_limit`](#history_limit)
* [`undo`](#undo)
* [`redo`](#redo)
* [`go_to_last`](#go_to_last)
* [`go_to_index`](#go_to_index)
* [`go_to_timestamp`](#go_to_timestamp)
* [`export_history_to_dict`](#export_history_to_dict)
* [`import_history_from_dict`](#import_history_from_dict)
* [`remove_history_limit`](#remove_history_limit)
* [`diff`](#diff)

---

### `init_mixins`

Sets up empty history state and records the instance's own starting state as the
first entry.

**Parameters:**
* *(none)*

**Returns:**
* `None`

**Under the hood:**
```python
def init_mixins(self):
    super().init_mixins()
    self._history = []
    self._history_limit = None
    self._history_index = 0
    self._history_count = 0
    self.record_state()
```

[▲ Back to top](#-table-of-contents)

---

### `record_state`

Creates a snapshot of the current state and saves it to history.

**Parameters:**
* *(none)*

**Returns:**
* `HistoryEntry`

**Example usage:**
```python
person.first_name = "Bob"
person.record_state()
```

**Under the hood:**
```python
def record_state(self):
    return record_state(self)
```

[▲ Back to top](#-table-of-contents)

---

### `history`

Returns the full history as a tuple.

**Parameters:**
* *(none — property getter)*

**Returns:**
* `tuple[HistoryEntry, ...]`

**Under the hood:**
```python
@property
def history(self):
    return tuple(self._history)
```

[▲ Back to top](#-table-of-contents)

---

### `history_index`

Returns the index of the currently active history entry.

**Parameters:**
* *(none — property getter)*

**Returns:**
* `int | None`

**Under the hood:**
```python
@property
def history_index(self):
    return self._history_index
```

[▲ Back to top](#-table-of-contents)

---

### `history_limit`

Gets or sets the history size limit.

**Parameters (setter):**
* `value` (*int*): the new limit.

**Returns:**
* `int | None` (getter)

**Example usage:**
```python
person.history_limit = 50
```

**Under the hood:**
```python
@property
def history_limit(self):
    return self._history_limit

@history_limit.setter
def history_limit(self, value):
    set_history_limit(self, value)
```

[▲ Back to top](#-table-of-contents)

---

### `undo`

Moves to the previous history entry, if one exists.

**Parameters:**
* *(none)*

**Returns:**
* `bool`: whether the move succeeded.

**Example usage:**
```python
person.undo()
```

**Under the hood:**
```python
def undo(self):
    return history_undo(self)
```

[▲ Back to top](#-table-of-contents)

---

### `redo`

Moves to the next history entry, if one exists.

**Parameters:**
* *(none)*

**Returns:**
* `bool`

**Example usage:**
```python
person.redo()
```

**Under the hood:**
```python
def redo(self):
    return history_redo(self)
```

[▲ Back to top](#-table-of-contents)

---

### `go_to_last`

Moves to the last recorded history entry.

**Parameters:**
* *(none)*

**Returns:**
* `None`

**Under the hood:**
```python
def go_to_last(self):
    go_to_last_history(self)
```

[▲ Back to top](#-table-of-contents)

---

### `go_to_index`

Moves to a specific history index.

**Parameters:**
* `index` (*int*)

**Returns:**
* `None`

**Under the hood:**
```python
def go_to_index(self, index):
    go_to_history_on_index(self, index)
```

[▲ Back to top](#-table-of-contents)

---

### `go_to_timestamp`

Moves to the history entry closest to a given timestamp.

**Parameters:**
* `timestamp` (*datetime*)

**Returns:**
* `None`

**Under the hood:**
```python
def go_to_timestamp(self, timestamp):
    go_to_history_on_timestamp(self, timestamp)
```

[▲ Back to top](#-table-of-contents)

---

### `export_history_to_dict`

Exports the full history to a dict, for persistence or transfer.

**Parameters:**
* *(none)*

**Returns:**
* `HistoryDict`

**Under the hood:**
```python
def export_history_to_dict(self):
    return export_history_to_dict(self)
```

[▲ Back to top](#-table-of-contents)

---

### `import_history_from_dict`

Imports a previously exported history dict, restoring it in place.

**Parameters:**
* `history_dict` (*HistoryDict*)

**Returns:**
* `None`

**Under the hood:**
```python
def import_history_from_dict(self, history_dict):
    import_history_from_dict(self, history_dict)
```

[▲ Back to top](#-table-of-contents)

---

### `remove_history_limit`

Removes the history size limit entirely.

**Parameters:**
* *(none)*

**Returns:**
* `None`

**Under the hood:**
```python
def remove_history_limit(self):
    self._history_limit = None
```

[▲ Back to top](#-table-of-contents)

---

### `diff`

Compares two recorded snapshots (by index or timestamp) and returns the changed
`(path, old_value, new_value)` triples.

**Parameters:**
* `snap1` (*int | datetime*): first snapshot selector.
* `snap2` (*int | datetime*): second snapshot selector.
* `constants_only` (*bool*, keyword-only, default `False`)

**Returns:**
* `SnapshotDiffTuple`

**Example usage:**
```python
person.diff(0, 3)
person.diff(some_timestamp, "now")
```

**Under the hood:**
```python
def diff(self, snap1, snap2, *, constants_only=False):
    return self._compare_snapshots(
        find_snapshot(self, snap1),
        find_snapshot(self, snap2),
        constants_only=constants_only
    )
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to Mixins Overview](../../../README_MIXINS_OVERVIEW.md)
