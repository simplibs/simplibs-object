# 🧱 `Serialization` — Universal Import/Export API

`Serialization` is the universal, "master" import/export mixin — `to_dict()` /
`to_json()` for reading an instance out as plain data, and `from_dict()` /
`from_json()` / `update_constants()` for rebuilding or updating one from plain data. It
automatically respects mutable-vs-immutable mode without branching itself.

```python
from src.simplibs.object.mixins.base_class import SimpleMixin
from .NodesTuple import NodesTuple
from .NodesDicts import NodesDicts
from .Snapshot import Snapshot

class Serialization(Snapshot, NodesDicts, NodesTuple, SimpleMixin):
    ...
```

---

## 🧭 Table of Contents

* [`to_dict`](#to_dict)
* [`to_json`](#to_json)
* [`from_dict`](#from_dict)
* [`from_json`](#from_json)
* [`update_constants`](#update_constants)

[⬅️ Back to main Mixins Overview](../README_MIXINS_OVERVIEW.md)

---

### `to_dict`

Serializes the instance into a readable flat dict.

**Parameters:**
* `constant_only` (*bool*, keyword-only, default `False`): if `True`, only constants
  (atoms) are included.

**Returns:**
* `StateDict`: a flat dict representation of the instance.

**Example usage:**
```python
data = person.to_dict()
# {"first_name": "Alice", "last_name": "Smith"}
```

**Under the hood:**
```python
def to_dict(self, *, constant_only: bool = False) -> dict:
  
    # 1. Define base variables with serializable class name
    result = {"_owner_class": self.meta.class_name}
    last_composite_key = UNSET
    last_composite_dict = {}

    # 2. Iterate through nodes_tuple in structural order
    for instance, path in self._nodes_tuple:

        # 2.1 Define per-node variables
        value = instance._value
        current_dict = result
        last_key = path[0] if path else instance.meta.name_snake

        # 2.2 Handle composite nodes (non-root)
        if len(path) > 1:

            # 2.2.1 Extract last and second-to-last keys
            last_key = path[-1]
            before_last_key = path[-2]

            # 2.2.2 Reuse previously cached composite dictionary
            if last_composite_key == before_last_key:
                current_dict = last_composite_dict

            # 2.2.3 Create a new composite dictionary
            else:

                # 2.2.3.1 Build nested structure for all keys except the last
                for key in path[:-1]:
                    current_dict = current_dict.setdefault(key, {})

                # 2.2.3.2 Cache composite dictionary for next iteration
                if last_key == "_value":
                    last_composite_key = before_last_key
                    last_composite_dict = current_dict

        # 2.3 Write the node value (unless filtered out)
        if not (constant_only and last_key == "_value"):
            current_dict[last_key] = value

    # 3. Return the final dictionary
    return result
```

[▲ Back to top](#-table-of-contents)

---

### `to_json`

Serializes the instance into a JSON string, via `to_dict()`.

**Parameters:**
* `**kwargs`: forwarded to `json.dumps`.

**Returns:**
* `str`: JSON representation of the instance.

**Example usage:**
```python
json_str = person.to_json(indent=2)
```

**Under the hood:**
```python
def to_json(self, **kwargs) -> str:
    return json.dumps(self.to_dict(), ensure_ascii=False, **kwargs)
```

[▲ Back to top](#-table-of-contents)

---

### `from_dict`

Reconstructs the instance's state from a dict. Mutable instances are updated in place;
immutable instances return a new instance.

**Parameters:**
* `user_dict` (*StateDict*): the dict to reconstruct from.

**Returns:**
* `SerializationProtocol`: `self` (mutable) or a new instance (immutable).

**Example usage:**
```python
person = person.from_dict({"first_name": "Bob"})
```

**Under the hood:**
```python
def from_dict(self, user_dict: dict) -> "Serialization":

    # 1. Validate input type
    if not isinstance(user_dict, dict):
        raise_unvalid_state_dict_input(self, user_dict)

    # 2. Validate owner class (supports both string class_name and class reference)
    owner_class = user_dict.get("_owner_class", UNSET)
    if owner_class not in (self.meta.class_name, self.meta.owner_class):
        raise_unvalid_owner_class_mismatch_for_state_dict(self, owner_class)

    # 3. Prepare traversal structures
    values = []
    last_composite_key = UNSET
    last_composite_dict = {}

    # 4. Load and validate values according to the _nodes_tuple structure
    for instance, path in self._nodes_tuple:

        # 4.1 Define per-node variables
        current_dict = user_dict
        last_key = path[-1] if path else instance.meta.name_snake

        # 4.2 Handle composite nodes (non-root)
        if len(path) > 1:

            # 4.2.1 Extract second-to-last key
            before_last_key = path[-2]

            # 4.2.2 Reuse previously cached composite dictionary
            if last_composite_key == before_last_key:
                current_dict = last_composite_dict

            # 4.2.3 Traverse into a new composite dictionary
            else:

                # 4.2.3.1 Traverse into nested dictionaries
                for key in path[:-1]:
                    current_dict = current_dict.get(key, UNSET)
                    if current_dict is UNSET:
                        raise_missing_composite_key(self, key, path)
                    if not isinstance(current_dict, dict):
                        raise_invalid_composite_structure(self, key, current_dict, path)

                # 4.2.3.2 Cache composite dictionary for next iteration
                if last_key == "_value":
                    last_composite_key = before_last_key
                    last_composite_dict = current_dict

        # 4.3 Load value
        value = current_dict.get(last_key, UNSET)
        if value is UNSET:
            raise_missing_value_key(self, last_key, path)

        # 4.4 Validate and store value
        instance.validate(value)
        values.append(value)

    # 5. Mutable mode → write values in-place
    if self.__is_mutable__:
        for (instance, _), value in zip(self._nodes_tuple, values):
            instance._value = value
        return self

    # 6. Immutable mode → create new instance from snapshot
    new_snapshot = tuple(values)
    return create_new_instance(self, new_snapshot)
```

[▲ Back to top](#-table-of-contents)

---

### `from_json`

Reconstructs the instance's state from a JSON string, via `from_dict()`.

**Parameters:**
* `json_str` (*str*): the JSON string to reconstruct from.

**Returns:**
* `SerializationProtocol`: `self` (mutable) or a new instance (immutable).

**Example usage:**
```python
person = person.from_json('{"first_name": "Bob"}')
```

**Under the hood:**
```python
def from_json(self, json_str: str) -> "Serialization":
    return self.from_dict(json.loads(json_str))
```

[▲ Back to top](#-table-of-contents)

---

### `update_constants`

Updates only the constants (atoms) from a possibly partial dict.

**Parameters:**
* `user_dict` (*StateDict*): a partial dict containing only constant fields to update.

**Returns:**
* `SerializationProtocol`: `self` (mutable) or a new instance (immutable).

**Example usage:**
```python
person = person.update_constants({"first_name": "Bob"})
```

**Under the hood:**
```python
def update_constants(self, user_dict: dict) -> "Serialization":
  
    # 1. Validate dictionary input
    if not isinstance(user_dict, dict):
        raise_unvalid_state_dict_input(self, user_dict)

    # 2. Prepare list for collecting changes (immutable mode)
    changes: list[tuple[str, object]] = []

    # 3. Traverse all nodes and search for values
    for instance, path in self._nodes_tuple:

        # 3.1 Skip composite "_value" nodes (only pure constants matter)
        if path and path[-1] == "_value":
            continue

        name = instance.meta.name_snake

        # 3.2 Direct lookup by atom name first, then fallback to nested path traversal
        if name in user_dict:
            current = user_dict[name]
        else:
            target_path = path if path else (name,)
            current = user_dict
            for key in target_path:
                current = current.get(key, UNSET)
                if not isinstance(current, dict) and key != target_path[-1]:
                    current = UNSET
                    break

        # 3.3 If a value was found → branch based on mutability
        if current is not UNSET:

            # 3.3.1 MUTABLE MODE → write directly in-place
            if self.__is_mutable__:
                instance.value = current

            # 3.3.2 IMMUTABLE MODE → collect changes for batch update
            else:
                changes.append((name, current))

    # 4. Handle mutable mode (and immutable mode with no changes)
    if self.__is_mutable__ or not changes:
        return self

    # 5. Handle immutable mode with collected changes
    return with_constants(self, tuple(changes))
   ```

[▲ Back to top](#-table-of-contents)

---

