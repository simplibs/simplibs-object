from typing import Any, TYPE_CHECKING
# Inners
from .vaidations import raise_immutability_constant_not_found
from .utils import (
    create_snapshot_dict,
    create_new_instance,
    reacalculate_owner_value,
)
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.core_mixins import (
        InfrastructureProtocol,
        InfrastructuredComponent,
    )


def with_constant(
    self: "InfrastructureProtocol",
    name: str,
    new_value: Any,
) -> "InfrastructuredComponent":
    """
    Integration requirement:
    This function is designed for the core pipeline framework. The object
    provided in `self` MUST inherit from:
      1. Snapshot (provides _restore_snapshot)
      2. NodesDicts (provides metadata and node access)
    Without these mixins, the pipeline will raise AttributeError.
    """

    # 1. Validate constant name
    if name not in self._constant_names_set:
        raise_immutability_constant_not_found(self, name)

    # 2. Validate new value
    instance, path = self._nodes_dict[name]
    instance.validate(new_value)

    # 3. Create current snapshot dictionary
    snapshot_dict = create_snapshot_dict(self._nodes_tuple)

    # 4. Write new constant value
    snapshot_dict[name] = new_value

    # 5. Recalculate composite values
    reacalculate_owner_value(snapshot_dict, instance.owner)

    # 6. Build clean snapshot tuple
    new_snapshot = tuple(snapshot_dict.values())

    # 7. Return new instance
    return create_new_instance(self, new_snapshot)


_DESIGN_NOTES = """
# with_constant

## Purpose
Updates a single constant (atomic node) in an immutable-safe way. This function
is the smallest unit of the immutability pipeline and is used whenever a single
constant value needs to be changed while ensuring composite nodes remain
consistent.

## Architectural role
This function is a core part of the immutability subsystem and is used by:

- [with_constants](ca://s?q=Explain_with_constants) — batch constant updates  
- [with_composite](ca://s?q=Explain_with_composite) — composite-level updates  
- [with_any](ca://s?q=Explain_with_any) — mixed updates  
- [Serialization update_constants](ca://s?q=Explain_update_constants) — partial dict updates  
- [Snapshot restoration](ca://s?q=Explain_snapshot_restoration) — rebuilding state  

It provides a deterministic, safe, and minimal update mechanism for atomic
values.

## How it works
The function performs seven deterministic steps:

1. **Validate constant name**  
   Ensures the target is a true constant, not a composite node.

2. **Validate new value**  
   Uses the node’s own validation logic to ensure type and semantic correctness.

3. **Create snapshot dictionary**  
   Builds a flat dictionary of current values using  
   [create_snapshot_dict](ca://s?q=Explain_create_snapshot_dict).

4. **Write new constant value**  
   Updates the snapshot dictionary at the constant’s name.

5. **Recalculate composite values**  
   Ensures structural consistency using  
   [reacalculate_owner_value](ca://s?q=Explain_recalculate_owner_value).

6. **Build clean snapshot tuple**  
   Converts the dictionary into a positional snapshot matching `nodes_tuple`.

7. **Return new instance**  
   Creates a new immutable instance using  
   [create_new_instance](ca://s?q=Explain_create_new_instance).

## Why this function exists
Immutable updates must:

- avoid mutating the original instance,
- preserve structural metadata,
- recalculate composite nodes,
- produce a fully initialized new instance.

`with_constant` encapsulates this entire process in a minimal, predictable
pipeline.

## Deterministic behavior
The update is deterministic because:

- `nodes_tuple` defines stable ordering,
- snapshot dictionaries use canonical `name_snake` keys,
- composite recalculation is pure,
- instance creation is clean and side-effect-free.

This determinism is essential for immutability, history tracking, and debugging.

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

Therefore, `with_constant` is treated as a **core invariant** of the immutability subsystem.

## Notes
- This function is intentionally minimal and side-effect-free.
- It is not part of the public API; it is used internally by mixins.
- All structural logic is delegated to helper utilities.
"""