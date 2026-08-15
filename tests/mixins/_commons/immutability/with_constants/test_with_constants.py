from typing import TYPE_CHECKING
# Outers
from ..with_constant.utils import (
    create_snapshot_dict,
    create_new_instance,
    reacalculate_owner_value,
)
# Inners
from .utils import find_longest_keys
from .vaidations import (
    raise_immutability_constants_changes_not_tuple,
    raise_immutability_batch_constant_not_found,
    validate_inner_tuple_name_is_str,
    validate_inner_tuple_is_tuple,
    validate_inner_tuple_has_length_two
)
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.alias_typings import ChangeTuple, ChangesTuple
    from ....._core.protocols.mixins.core_mixins import (
        InfrastructureProtocol,
        InfrastructuredComponent,
    )


def with_constants(
    self: "InfrastructureProtocol",
    changes: "ChangeTuple | ChangesTuple | None" = None,
) -> "InfrastructuredComponent":
    """
    Integration requirement:
    This function is designed for the core pipeline framework. The object
    provided in `self` MUST inherit from:
      1. Snapshot (provides _restore_snapshot)
      2. NodesDicts (provides metadata and node access)
    Without these mixins, the pipeline will raise AttributeError.
    """

    # 1. Create current snapshot dictionary
    snapshot_dict = create_snapshot_dict(self._nodes_tuple)

    # 2. Prepare dictionary for path tracking
    path_dict = {}

    # 3. Build initial snapshot
    new_snapshot = self._build_snapshot()

    # 4. Apply changes if provided
    if changes:

        # 4.1 Validate that input is a tuple
        if not isinstance(changes, tuple):
            raise_immutability_constants_changes_not_tuple(self, changes)

        # 4.2 Normalize input if single change was provided
        if not isinstance(changes[0], tuple):
            changes = (changes,)

        # 4.3 Process each inner tuple
        for inner_tuple in changes:

            # 4.3.1 Validate tuple structure
            if (
                not isinstance(inner_tuple, tuple)
                or len(inner_tuple) != 2
                or not isinstance(inner_tuple[0], str)
            ):
                validate_inner_tuple_is_tuple(self, inner_tuple)
                validate_inner_tuple_has_length_two(self, inner_tuple)
                validate_inner_tuple_name_is_str(self, inner_tuple)

            # 4.3.2 Extract variables
            inner_name, new_value = inner_tuple

            # 4.3.3 Validate that the name refers to a constant
            if inner_name not in self._constant_names_tuple:
                raise_immutability_batch_constant_not_found(self, inner_name)

            # 4.3.4 Validate new value
            instance, path = self._nodes_dict[inner_name]
            instance.validate(new_value)

            # 4.3.5 Write new value into snapshot dictionary
            snapshot_dict[inner_name] = new_value

            # 4.3.6 Store path for recalculation
            path_dict[inner_name] = path

        # 4.4 Extract deepest affected keys
        longest_key = find_longest_keys(path_dict)

        # 4.5 Recalculate composite values starting from deepest nodes
        for key in longest_key:
            instance = self._nodes_instance_dict[key]
            reacalculate_owner_value(snapshot_dict, instance.owner)

        # 4.6 Build clean snapshot tuple
        new_snapshot = tuple(snapshot_dict.values())

    # 5. Return new instance
    return create_new_instance(self, new_snapshot)


_DESIGN_NOTES = """
# with_constants

## Purpose
Applies multiple constant updates in a single immutable-safe operation.
This function is the batch version of [with_constant](ca://s?q=Explain_with_constant) and is used whenever several atomic values must be updated at once while ensuring composite nodes remain consistent.

## Architectural role
This function is used by:

- [with_any](ca://s?q=Explain_with_any) — mixed updates  
- [with_composite](ca://s?q=Explain_with_composite) — composite updates  
- [Serialization update_constants](ca://s?q=Explain_update_constants) — partial dict updates  
- [Snapshot restoration](ca://s?q=Explain_snapshot_restoration) — rebuilding state  

It provides a deterministic, safe, and efficient batch update mechanism.

## How it works
The function performs five deterministic phases:

### 1. Build snapshot dictionary
Uses [create_snapshot_dict](ca://s?q=Explain_create_snapshot_dict) to create a flat dictionary of current values.

### 2. Prepare path dictionary
Stores structural paths of changed constants for later recalculation.

### 3. Normalize and validate changes
Each change must be a `(name, value)` tuple.  
Validation ensures:

- correct tuple structure,  
- constant name correctness,  
- semantic correctness via `validate()`.

### 4. Apply changes and recalculate composites
After writing new constant values:

- affected paths are analyzed using  
  [find_longest_keys](ca://s?q=Explain_find_longest_keys)  
- composite recalculation begins at deepest nodes using  
  [reacalculate_owner_value](ca://s?q=Explain_recalculate_owner_value)

This guarantees correct dependency ordering.

### 5. Build clean snapshot and create new instance
The updated dictionary is converted into a positional snapshot and passed to  
[create_new_instance](ca://s?q=Explain_create_new_instance).

## Why batch updates matter
Batch updates allow:

- atomic multi-value changes,  
- correct composite recalculation,  
- minimal recomputation,  
- deterministic immutability behavior,  
- efficient pipelines for serialization and patch operations.

## Deterministic behavior
The update is deterministic because:

- `nodes_tuple` defines stable ordering,  
- snapshot dictionaries use canonical `name_snake` keys,  
- composite recalculation is pure,  
- terminal nodes are computed structurally,  
- instance creation is clean and side-effect-free.

## Integration requirements
The function assumes the instance implements:

- [Snapshot](ca://s?q=Explain_Snapshot_mixin) — provides `_restore_snapshot`  
- [NodesDicts](ca://s?q=Explain_NodesDicts_mixin) — provides node metadata  

Without these mixins, the pipeline cannot reconstruct the instance.

## Stability guarantee
Any change to this function would affect:

- immutability behavior,  
- composite recalculation,  
- serialization consistency,  
- debugging tools,  
- history tracking.

Therefore, `with_constants` is treated as a **core invariant** of the immutability subsystem.

## Notes
- This function is intentionally minimal and side-effect-free.  
- It is not part of the public API; it is used internally by mixins.  
- All structural logic is delegated to helper utilities.
"""