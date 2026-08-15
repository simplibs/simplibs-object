from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Outers
from ...._common_logic.constants import VALUE
from ...._common_logic.immutability import with_constants
# Inners
from .validations import raise_unvalid_state_dict_input
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.core_mixins import SerializationProtocol
    from ....._core.protocols.alias_typings import StateDict


def from_dict_constants(
    self: "SerializationProtocol",
    user_dict: "StateDict",
) -> "SerializationProtocol":
    """
    Updates the object's constant (atomic) values from a partial or full dictionary.

    Automatically detects the object's operational mode:
    - Mutable mode: updates values in-place.
    - Immutable mode: returns a new instance with applied changes.
    """

    # 1. Validate dictionary input
    if not isinstance(user_dict, dict):
        raise_unvalid_state_dict_input(self, user_dict)

    # 2. Prepare list for collecting changes (immutable mode)
    changes: list[tuple[str, object]] = []

    # 3. Traverse all nodes and search for values according to their paths
    for instance, path in self._nodes_tuple:

        # 3.1 Skip composite VALUE nodes (only pure constants matter)
        if path[-1] == VALUE:
            continue

        # 3.2 Search for the value deep inside the user dictionary
        current = user_dict
        for key in path:
            current = current.get(key, UNSET)
            if not isinstance(current, dict) and key != path[-1]:
                current = UNSET
                break

        # 3.3 If a value was found → branch based on mutability
        if current is not UNSET:

            # 3.3.1 MUTABLE MODE → write directly in-place
            if self.__is_mutable__:
                instance.value = current

            # 3.3.2 IMMUTABLE MODE → collect changes for batch update
            else:
                name = instance.meta.name_snake
                changes.append((name, current))

    # 4. Handle mutable mode (and immutable mode with no changes)
    if self.__is_mutable__ or not changes:
        return self

    # 5. Handle immutable mode with collected changes
    return with_constants(self, tuple(changes))


_DESIGN_NOTES = """
# from_dict_constants

## Purpose
Updates only the **constant (atomic)** values of an object using a partial or
full dictionary. This function is the lightweight counterpart to `from_dict`,
focusing exclusively on constants and ignoring composite VALUE nodes.

It supports both operational modes:

- **mutable mode** — updates values directly in-place  
- **immutable mode** — returns a new instance with updated constants  

This makes it ideal for targeted updates where only atomic values change.

## Architectural role
`from_dict_constants` is used by:

- `SerializationMixin` (`update_constants`)
- immutability pipelines (`with_constants`)
- debugging tools
- partial state restoration
- external integrations (patch-like updates)

It provides a safe and deterministic way to update constants without touching
composite structure.

## Traversal logic
The function walks through `_nodes_tuple` and:

1. **skips composite VALUE nodes**, because constants are the only target  
2. **traverses the user dictionary** according to each node’s path  
3. **validates dictionary structure**  
4. **detects missing or malformed paths**  
5. **collects or applies values** depending on mutability  

This ensures that updates respect the object’s structural layout.

## Mutable vs immutable behavior
### Mutable mode
- values are written directly into the existing instance  
- no new object is created  
- changes happen immediately  

### Immutable mode
- changes are collected into a list of `(name, value)` pairs  
- `with_constants(self, changes)` creates a new instance  
- original instance remains unchanged  

This dual behavior is consistent with the entire Simple object model.

## Partial dictionary support
The function accepts **partial dictionaries**:

- missing constants are ignored  
- only provided constants are updated  
- composite structure is not required  

This makes it ideal for patch operations.

## Stability guarantee
This function is a core part of the Simple serialization subsystem.  
Any change affects:

- constant updates  
- immutability pipelines  
- JSON import  
- debugging tools  
- external integrations  

Therefore, `from_dict_constants` is treated as a **structural invariant**.

## Notes
- This function is intentionally low-level and not part of the public API.  
- All structural logic is delegated to `_nodes_tuple`.  
- All immutable update logic is delegated to `with_constants`.  

"""