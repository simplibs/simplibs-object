from typing import Any, TYPE_CHECKING
# Outers
from ..with_composite import with_composite
from ..with_constants import with_constants
from ..with_constant.utils import create_new_instance, create_snapshot_dict
# Inners
from .utils import (
    get_top_composite_paths,
    split_constants_paths,
    process_single_change,
    split_changes,
)
from .vaidations import (
    raise_with_any_changes_is_not_tuple,
    raise_with_any_child_composite_mismatch,
    raise_with_any_contained_constant_mismatch,
)
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.alias_typings import ChangeTuple, ChangesTuple
    from ....._core.protocols.mixins.core_mixins import (
        InfrastructureProtocol,
        InfrastructuredComponent,
    )


def with_any(
    self: "InfrastructureProtocol",
    changes: "ChangeTuple | ChangesTuple | None" = None,
) -> "InfrastructuredComponent | Any":
    """
    Integration requirement:
    This function is designed for the core pipeline framework. The object
    provided in `self` MUST inherit from:
      1. Snapshot (provides _restore_snapshot)
      2. NodesDicts (provides metadata and node access)
    Without these mixins, the pipeline will raise AttributeError.
    """

    # 1. Handle case with no changes
    if not changes:
        instance = create_new_instance(self, self._build_snapshot())
        return instance if not self.__is_mutable__ else instance.value

    # 2. Validate type of changes
    if not isinstance(changes, tuple):
        raise_with_any_changes_is_not_tuple(self, changes)

    # 3. Handle single change
    if not isinstance(changes[0], tuple):
        changes: tuple[str, Any]
        instance = process_single_change(self, changes)
        return instance if not self.__is_mutable__ else instance.value

    # 4. Split changes into constants and composites
    changes: tuple[tuple[str, Any], ...]
    constants, composite = split_changes(self, changes)

    # 5. If all changes are constants → delegate
    if not composite:
        instance = with_constants(self, changes)
        return instance if not self.__is_mutable__ else instance.value

    # 6. Build dictionary of provided values
    changes_dict = {key: value for key, value in changes}

    # 7. Determine top-level and child composite paths
    top_composite, child_composite = get_top_composite_paths(
        composite,
        self._nodes_path_dict,
    )

    # 8. Create base instance
    instance = create_new_instance(self, self._build_snapshot())

    # 9. Apply root composites
    for name in top_composite:
        instance = with_composite(instance, name, changes_dict[name])

    # 10. Snapshot after root composites
    # noinspection PyProtectedMember
    instance_snapshot_dict = create_snapshot_dict(instance._nodes_tuple)

    # 11. Validate child composites
    if child_composite:
        for name, value in composite:
            if instance_snapshot_dict[name] != value:
                raise_with_any_child_composite_mismatch(
                    self, name, value, instance_snapshot_dict[name]
                )

    # 12. Process constants
    if constants:

        # 12.1 Split into contained and unique constants
        contained, unique = split_constants_paths(
            constants,
            top_composite,
            self._nodes_path_dict,
        )

        # 12.2 Validate contained constants
        for name in contained:
            if instance_snapshot_dict[name] != changes_dict[name]:
                raise_with_any_contained_constant_mismatch(
                    self, name, changes_dict[name], instance_snapshot_dict[name]
                )

        # 12.3 Apply unique constants
        if unique:
            new_changes = [(name, changes_dict[name]) for name in unique]
            instance = with_constants(instance, tuple(new_changes))

    # 13. Return instance or value (mutable mode)
    return instance if not self.__is_mutable__ else instance.value


_DESIGN_NOTES = """
# with_any

## Purpose
Provides a unified entry point for **any type of update** — constants, composites,
or mixed updates.  
This is the highest-level immutability function and orchestrates all update
pipelines:

- [with_constant](ca://s?q=Explain_with_constant)  
- [with_constants](ca://s?q=Explain_with_constants)  
- [with_composite](ca://s?q=Explain_with_composite)  
- and all helper functions in the `with_any` subsystem.

It ensures that updates are applied in the correct structural order and that
the resulting instance is fully consistent.

## Architectural role
This function is used by:

- user-facing APIs (`__call__`, update methods)  
- serialization pipelines  
- patch operations  
- debugging and diffing tools  

It is the **central dispatcher** for immutability updates.

## How it works
The function performs thirteen deterministic phases:

### 1. Handle no changes
Returns a fresh instance (immutable mode) or its value (mutable mode).

### 2. Validate input type
Ensures the update is a tuple.

### 3. Handle single change
Delegates to [process_single_change](ca://s?q=Explain_process_single_change).

### 4. Split changes
Uses [split_changes](ca://s?q=Explain_split_changes) to classify constants and composites.

### 5. If only constants → delegate
Uses [with_constants](ca://s?q=Explain_with_constants).

### 6. Build dictionary of provided values
Used for composite and constant validation.

### 7. Determine composite hierarchy
Uses [get_top_composite_paths](ca://s?q=Explain_get_top_composite_paths) to find:

- root composites → applied first  
- child composites → validated later  

### 8. Create base instance
Fresh instance ensures immutability.

### 9. Apply root composites
Uses [with_composite](ca://s?q=Explain_with_composite).

### 10. Build snapshot after composite updates
Used for validation.

### 11. Validate child composites
Ensures composite updates are structurally consistent.

### 12. Process constants
Uses [split_constants_paths](ca://s?q=Explain_split_constants_paths) to classify:

- contained constants → validated against composite decomposition  
- unique constants → applied via `with_constants`  

Then applies unique constants via [with_constants](ca://s?q=Explain_with_constants).

### 13. Return instance or value
Supports mutable mode (`__is_mutable__`).

## Why this function exists
Mixed updates require:

- correct ordering (composites → constants),  
- structural validation,  
- dependency-aware recalculation,  
- minimal recomputation,  
- deterministic immutability behavior.

`with_any` encapsulates all of this in a single, predictable pipeline.

## Deterministic behavior
The update is deterministic because:

- composite hierarchy is computed structurally,  
- constants are validated against composite results,  
- snapshot dictionaries use canonical `name_snake` keys,  
- instance creation is clean and side-effect-free,  
- helper functions are pure and stable.

## Integration requirements
The function assumes the instance implements:

- [Snapshot](ca://s?q=Explain_Snapshot_mixin) — provides `_restore_snapshot`  
- [NodesDicts](ca://s?q=Explain_NodesDicts_mixin) — provides node metadata  

Without these mixins, the pipeline cannot reconstruct the instance.

## Stability guarantee
Any change to this function would affect:

- immutability behavior,  
- composite recalculation order,  
- serialization consistency,  
- debugging tools,  
- patch operations.

Therefore, `with_any` is treated as a **core invariant** of the immutability subsystem.

## Notes
- This function is intentionally minimal and side-effect-free.  
- It is not part of the public API; it is used internally by mixins.  
- All structural logic is delegated to helper utilities.
"""