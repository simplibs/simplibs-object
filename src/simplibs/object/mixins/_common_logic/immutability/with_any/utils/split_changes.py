from typing import Any, TYPE_CHECKING
# Outers
from ...with_constants.vaidations import (
    validate_inner_tuple_is_tuple,
    validate_inner_tuple_has_length_two,
    validate_inner_tuple_name_is_str
)
# Inners
from .validations import raise_split_changes_unknown_name
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.core_mixins import InfrastructureProtocol
    from ......_core.protocols.alias_typings import ChangesTuple


def split_changes(
    self: "InfrastructureProtocol",
    changes: "ChangesTuple",
) -> tuple["ChangesTuple", "ChangesTuple"]:
    """
    Splits incoming changes into:
        - constants: [(name, value), ...]
        - composite: [(name, value), ...]

    Also performs structural validation.
    """

    constants = []
    composite = []

    for inner_tuple in changes:

        # 1. Validate tuple structure
        if (
            not isinstance(inner_tuple, tuple)
            or len(inner_tuple) != 2
            or not isinstance(inner_tuple[0], str)
        ):
            validate_inner_tuple_is_tuple(self, inner_tuple)
            validate_inner_tuple_has_length_two(self, inner_tuple)
            validate_inner_tuple_name_is_str(self, inner_tuple)

        name = inner_tuple[0]

        # 2. Constant
        if name in self._constant_names_set:
            constants.append(inner_tuple)

        # 3. Composite
        elif name in self.meta.node_names_set:
            composite.append(inner_tuple)

        # 4. Unknown name
        else:
            raise_split_changes_unknown_name(self, name)

    return tuple(constants), tuple(composite)


_DESIGN_NOTES = """
# split_changes

## Purpose
Separates incoming updates into **constant changes** and **composite changes**.
This function is the first structural step of the [with_any](ca://s?q=Explain_with_any) pipeline and ensures that mixed updates are processed in the correct order.

It also validates the structural correctness of each `(name, value)` tuple.

## Architectural role
This function is used by:

- [with_any](ca://s?q=Explain_with_any) — mixed update pipeline  
- indirectly by composite and constant update logic  
- debugging and validation tools  

It provides the minimal classification mechanism required for correct immutability behavior.

## How it works
The function performs four deterministic steps:

### 1. Validate tuple structure
Each change must be a `(name, value)` pair with a string name.  
Malformed updates are rejected immediately.

### 2. Classify constants
If the name belongs to `_constant_names_set`, the change is appended to the
constant list.

### 3. Classify composites
If the name belongs to `meta.node_names_set`, the change is appended to the
composite list.

### 4. Reject unknown names
If the name is neither a constant nor a composite, the update is invalid.

## Why classification matters
Mixed updates require different processing strategies:

- constants → validated individually, applied last  
- composites → applied first, may affect inner nodes and owners  

Correct classification ensures:

- deterministic update order,  
- correct composite recalculation,  
- minimal recomputation,  
- structural consistency.

## Deterministic behavior
The classification is deterministic because:

- metadata sets are canonical,  
- tuple validation is strict,  
- output ordering matches input ordering,  
- no side effects occur.

This determinism is essential for immutability pipelines.

## Integration requirements
The function assumes the instance implements:

- [NodesDicts](ca://s?q=Explain_NodesDicts_mixin) — provides node metadata  
- [Snapshot](ca://s?q=Explain_Snapshot_mixin) — indirectly used by downstream functions  

Without these mixins, the pipeline cannot classify updates correctly.

## Stability guarantee
Any change to this function would affect:

- routing logic in `with_any`,  
- composite recalculation order,  
- immutability correctness,  
- debugging behavior.

Therefore, `split_changes` is treated as a **core invariant** of the immutability subsystem.

## Notes
- This function is intentionally minimal and side-effect-free.  
- It is not part of the public API; it is used internally by mixins.  
- All structural logic is delegated to metadata (`_constant_names_set`, `node_names_set`).  

"""