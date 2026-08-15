from typing import Any, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.core_mixins import (
        InfrastructureProtocol,
        InfrastructuredComponent,
    )
    from ......_core.protocols.alias_typings import SnapshotTuple


def create_new_instance(
    instance: "InfrastructureProtocol",
    snapshot: "SnapshotTuple",
) -> "InfrastructuredComponent":
    """
    Creates a new instance using the same class as the provided object,
    initializes it, and restores its state from the given snapshot.

    Integration requirement:
    The provided instance MUST inherit from:
      1. Snapshot (provides _restore_snapshot)
      2. NodesDicts (provides metadata and node access)
    Otherwise, the pipeline will raise AttributeError.
    """

    # 1. Create a new instance
    new_instance = object.__new__(type(instance))
    new_instance.__init__()
    new_instance: "InfrastructuredComponent"

    # 2. Load snapshot values
    # noinspection PyProtectedMember
    new_instance._restore_snapshot(snapshot)

    # 3. Return the new instance
    return new_instance


_DESIGN_NOTES = """
# create_new_instance

## Purpose
Creates a brand‑new instance of the same class as the provided object and
restores its internal state from a snapshot. This function is the backbone of
the immutable pipeline: every immutable update ultimately produces a new
instance through this mechanism.

## Architectural role
`create_new_instance` is used by:

- `with_constant`
- `with_constants`
- `with_composite`
- `with_any`
- snapshot restoration logic
- serialization import pipelines (immutable mode)

It ensures that immutable operations produce fully initialized, structurally
correct instances.

## How it works
The function performs three deterministic steps:

1. **Create a new instance**  
   Uses `object.__new__(type(instance))` to bypass `__init__` arguments and
   guarantee a clean, uninitialized object.

2. **Initialize the instance**  
   Calls `__init__()` to run all mixin initialization logic, including:
   - slot setup  
   - metadata construction  
   - nodes tuple building  
   - dictionary mappings  
   - composite structure preparation  

3. **Restore snapshot**  
   Calls `_restore_snapshot(snapshot)` to inject raw values into the new
   instance. This ensures the new object reflects the exact state encoded in
   the snapshot.

## Integration requirements
The function assumes that the instance implements:

- **SnapshotMixin**  
  Provides `_restore_snapshot(snapshot)`.

- **NodesDictsMixin**  
  Provides metadata, node access, and structural information.

Without these mixins, the pipeline cannot reconstruct the instance and will
raise `AttributeError`.

## Why this function exists
Immutable operations must:

- produce a new instance,
- preserve structural metadata,
- restore values deterministically,
- avoid mutating the original object.

This function encapsulates that entire process in a single, stable utility.

## Deterministic behavior
The new instance is guaranteed to be:

- structurally identical to the original,
- fully initialized,
- value‑correct according to the snapshot,
- safe for further immutable operations.

This determinism is essential for immutability pipelines, history tracking,
and debugging.

## Stability guarantee
Any change to this function would affect:

- immutable updates,
- snapshot restoration,
- serialization import,
- composite recalculation,
- debugging tools.

Therefore, `create_new_instance` is treated as a **core invariant** of the
immutability subsystem.

## Notes
- This function is intentionally minimal and side‑effect‑free.
- It is not part of the public API; it is used internally by mixins.
- All structural logic is delegated to mixin initialization.
"""