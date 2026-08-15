from typing import Any, TYPE_CHECKING
# Outers
from ..with_constant import with_constant
from ..with_constant.utils import (
    create_snapshot_dict,
    reacalculate_owner_value,
    create_new_instance,
)
# Inners
from .utils import reacalculate_inners
from .vaidations import (
    validate_composite_name_exists,
    validate_composite_is_decomposeable
)
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.core_mixins import (
        InfrastructureProtocol,
        InfrastructuredComponent,
    )


def with_composite(
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

    # 1. If the target is a constant → delegate to with_constant
    if name in self._constant_names_tuple:
        return with_constant(self, name, new_value)

    # 2. Validate composite name and decomposability
    if name not in self.meta.node_names_set or not self.meta.is_decomposeable:
        validate_composite_name_exists(self, name)
        validate_composite_is_decomposeable(self, name)

    # 3. Validate new composite value
    instance, path = self._nodes_dict[name]
    instance.validate(new_value)

    # 4. Create current snapshot dictionary
    snapshot_dict = create_snapshot_dict(self._nodes_tuple)

    # 5. Write new composite value
    snapshot_dict[name] = new_value

    # 6. Recalculate inner values
    reacalculate_inners(snapshot_dict, instance.meta, new_value)

    # 7. Recalculate composite owner values
    reacalculate_owner_value(snapshot_dict, instance.owner)

    # 8. Build clean snapshot tuple
    new_snapshot = tuple(snapshot_dict.values())

    # 9. Return new instance
    return create_new_instance(self, new_snapshot)


_DESIGN_NOTES = """
# with_composite

## Purpose
Updates a composite node in an immutable-safe way. This function is the
structural counterpart to [with_constant](ca://s?q=Explain_with_constant) and
is used whenever a composite value changes and must propagate through its
inner nodes and owner hierarchy.

It ensures that composite updates remain consistent, deterministic, and
structurally correct.

## Architectural role
This function is used by:

- [with_any](ca://s?q=Explain_with_any) — mixed updates  
- [with_constants](ca://s?q=Explain_with_constants) — batch constant updates  
- snapshot restoration  
- immutability pipelines  
- debugging and diffing tools  

It provides the core mechanism for updating composite nodes.

## How it works
The function performs nine deterministic steps:

### 1. Delegate constant updates
If the target name refers to a constant, the function delegates to  
[with_constant](ca://s?q=Explain_with_constant).

### 2. Validate composite name and decomposability
Ensures the node exists and is decomposable (`meta.is_decomposeable`).

### 3. Validate new composite value
Uses the node’s own validation logic to ensure semantic correctness.

### 4. Create snapshot dictionary
Builds a flat dictionary of current values using  
[create_snapshot_dict](ca://s?q=Explain_create_snapshot_dict).

### 5. Write new composite value
Updates the snapshot dictionary at the composite’s name.

### 6. Recalculate inner values
Uses [reacalculate_inners](ca://s?q=Explain_recalculate_inners) to propagate
the new composite value into all inner nodes — including nested composites.

### 7. Recalculate owner values
Uses [reacalculate_owner_value](ca://s?q=Explain_recalculate_owner_value) to
update the composite’s owner (and potentially higher-level composites).

### 8. Build clean snapshot tuple
Converts the updated dictionary into a positional snapshot matching
`nodes_tuple`.

### 9. Create and return new instance
Uses [create_new_instance](ca://s?q=Explain_create_new_instance) to produce a
fully initialized immutable instance.

## Why composite updates require two recalculation phases
Composite updates affect:

- **inner nodes** (via decomposition),  
- **owner nodes** (via composition).

Both directions must be updated to maintain structural consistency.

This two-phase recalculation ensures:

- correct propagation downward (inners),  
- correct propagation upward (owners),  
- deterministic immutability behavior.

## Deterministic behavior
The update is deterministic because:

- decomposition order is stable,  
- metadata ordering is canonical,  
- owner recalculation is pure,  
- snapshot dictionary uses canonical `name_snake` keys,  
- instance creation is clean and side-effect-free.

## Integration requirements
The function assumes the instance implements:

- [Snapshot](ca://s?q=Explain_Snapshot_mixin) — provides `_restore_snapshot`  
- [NodesDicts](ca://s?q=Explain_NodesDicts_mixin) — provides node metadata  

Without these mixins, the pipeline cannot reconstruct the instance.

## Stability guarantee
Any change to this function would affect:

- composite recalculation,  
- immutability correctness,  
- snapshot consistency,  
- debugging tools,  
- serialization behavior.

Therefore, `with_composite` is treated as a **core invariant** of the
immutability subsystem.

## Notes
- This function is intentionally minimal and side-effect-free.  
- It is not part of the public API; it is used internally by mixins.  
- All structural logic is delegated to helper utilities.

"""