# 🧱 `History` — Full Undo/Redo History

`History` provides a full undo/redo history for a mutable instance. State-changing
actions are recorded as timestamped snapshots, navigable step by step or by
index/timestamp, diffable between any two points, and exportable to/from a dict.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin
from src.simplibs.object.mixins.core_mixins import Serialization, Snapshot, NodesDicts, NodesTuple

class History(Serialization, Snapshot, NodesDicts, NodesTuple, SimpleMixin):
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
    
    # 1. Create timestamp and snapshot
    timestamp = datetime.now()
    snapshot = self._build_snapshot()

    # 2. Enforce history limit
    if self._history_limit and self._history_count >= self._history_limit:
        self._history.pop(0)

    # 3. Store entry
    history_entry = (timestamp, snapshot)
    self._history.append(history_entry)
    self._history_count = len(self._history)
    self._history_index = self._history_count - 1

    # 4. Return entry
    return history_entry
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

    # 1. Validate value
    if not isinstance(value, int) or value < 1:
        raise_history_limit_not_positive_integer(self, value)

    # 2. Adjust history to the new limit
    if self._history_count > value:
        del self._history[:(self._history_count - value)]
        self._history_count = len(self._history)
        self._history_index = self._history_count - 1

    # 3. Store limit
    self._history_limit = value
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

    # 1. Check if a backward move is possible
    if self._history_index <= 0:
        return False

    # 2. Move to the previous entry
    self._history_index -= 1
    _, snapshot = self._history[self._history_index]
    self._restore_snapshot(snapshot)
    return True
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

    # 1. Check if a forward move is possible
    if self._history_index >= self._history_count - 1:
        return False

    # 2. Move to the next entry
    self._history_index += 1
    _, snapshot = self._history[self._history_index]
    self._restore_snapshot(snapshot)
    return True
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

    # 1. Check if already at the last entry
    last_index = self._history_count - 1
    if self._history_index != last_index:

        # 2. Switch to the last entry
        self._history_index = last_index
        _, snapshot = self._history[self._history_index]
        self._restore_snapshot(snapshot)
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

    # 1. Validate index
    if not (0 <= index < self._history_count):
        raise_unvalide_snapshot_index(self, index)

    # 2. Switch to the selected entry
    self._history_index = index
    _, snapshot = self._history[self._history_index]
    self._restore_snapshot(snapshot)
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

    # 1. Validate timestamp type
    if not isinstance(timestamp, datetime):
        raise_unvalide_timestamp(self, timestamp)

    # 2. Search for matching timestamp
    for i, (ts, snapshot) in enumerate(self._history):
        if ts == timestamp:
            self._history_index = i
            self._restore_snapshot(snapshot)
            return

    # 3. Timestamp not found
    raise_unvalide_snopshot_timestamp(self, timestamp)
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
    return {
        "_owner_class": self.meta.owner_class,
        "history": self.history
    }
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

    # 1. Validate input type
    if not isinstance(history_dict, dict):
        raise_unvalide_history_import_file(self, history_dict)

    # 2. Validate owner class
    owner_class = history_dict.get("_owner_class", UNSET)
    if self.meta.owner_class != owner_class:
        raise_unvalide_owner_class_mismatch(self, owner_class)

    # 3. Backup previous history and state
    backup_history = list(self._history)
    backup_count = self._history_count
    backup_index = self._history_index

    # 4. Replace history
    try:
        # 4.1 Load new history and sync count
        self._history = list(history_dict["history"])
        self._history_count = len(self._history)

        # 4.2 Jump to the newest state
        self.go_to_last()

        # 4.3 Apply limit trimming (if configured)
        if self.history_limit:
            self.history_limit = self.history_limit

    # 5. Restore previous state on failure
    except Exception as e:
        self._history = backup_history
        self._history_count = backup_count
        self._history_index = backup_index
        self.go_to_last()
        raise e
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
