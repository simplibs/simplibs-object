from typing import TYPE_CHECKING
from simplibs.sentinels import UNSET
# Outers
from ...._common_logic.constants import OWNER_CLASS, VALUE
from ...._common_logic.immutability import create_new_instance
# Inners
from .validations import (
    raise_unvalid_state_dict_input,
    raise_unvalid_owner_class_mismatch_for_state_dict,
    raise_missing_composite_key,
    raise_invalid_composite_structure,
    raise_missing_value_key
)
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.core_mixins import SerializationProtocol
    from ....._core.protocols.alias_typings import StateDict


def from_dict(
    self: "SerializationProtocol",
    user_dict: "StateDict",
) -> "SerializationProtocol":
    """
    Universal reconstruction of instance state from a dictionary.
    Supports both mutable (in-place) and immutable (new instance) modes.
    """

    # 1. Validate input type
    if not isinstance(user_dict, dict):
        raise_unvalid_state_dict_input(self, user_dict)

    # 2. Validate owner class (supports both string class_name and class reference)
    owner_class = user_dict.get(OWNER_CLASS, UNSET)
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
                if last_key == VALUE:
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


_DESIGN_NOTES = """
# from_dict

## Purpose
Reconstructs the full state of an instance from a user‑provided dictionary.
This function is the central import mechanism of the Simple serialization
pipeline and supports both operational modes:

- **mutable mode** — values are written directly into the existing instance  
- **immutable mode** — a new instance is created from the reconstructed snapshot

This dual behavior allows the same API to be used consistently across all
Simple objects regardless of their mutability configuration.

## Architectural role
`from_dict` is used by:

- `SerializationMixin` (`from_dict`, `from_json`)
- immutability helpers (`create_new_instance`)
- debugging tools
- state restoration pipelines
- external integrations (JSON import, API payloads)

It ensures that external data can be safely mapped back into the internal
object structure defined by `nodes_tuple`.

## Input validation
The function performs strict validation:

1. **Input type**  
   The provided value must be a dictionary.

2. **Owner class identity**  
   The dictionary must contain the matching `OWNER_CLASS` token.  
   It accepts both string identifiers (`meta.class_name`) and class references (`meta.owner_class`),
   allowing transparent JSON restoration and in-memory Python dictionary restoration.

3. **Structural correctness**  
   The dictionary must contain all required keys according to the structural
   paths defined in `_nodes_tuple` (resolving standalone atoms via `name_snake`).

4. **Value validation**  
   Each value is validated using the instance’s own `validate()` method.

These checks guarantee that only structurally correct and type‑safe data enters
the object.

## Traversal logic
The function reconstructs values by walking the dictionary according to the
paths stored in `_nodes_tuple`.

To optimize traversal:

- standalone atom nodes with empty paths safely fallback to `instance.meta.name_snake`
- composite dictionaries are cached (`last_composite_dict`)
- repeated lookups into the same composite branch are avoided
- missing keys or invalid structures raise clear diagnostics

This ensures linear performance even for deeply nested composite objects.

## Mutable vs immutable behavior
After all values are collected and validated:

### Mutable mode
Values are written directly into the existing instance:

- no new object is created  
- changes happen in-place  
- the instance identity is preserved  

### Immutable mode
A new instance is created using:

- a freshly built snapshot  
- `create_new_instance(self, new_snapshot)`  

This ensures immutability guarantees while preserving the original instance.

## Stability guarantee
This function is a core part of the Simple serialization subsystem.  
Any change affects:

- JSON import  
- snapshot restoration  
- immutability pipelines  
- debugging tools  
- external integrations  

Therefore, `from_dict` is treated as a **structural invariant** of the system.

## Notes
- This function is intentionally low‑level and not part of the public API.  
- All structural logic is delegated to `_nodes_tuple`.  
- All instance creation logic is delegated to `create_new_instance`.  
"""