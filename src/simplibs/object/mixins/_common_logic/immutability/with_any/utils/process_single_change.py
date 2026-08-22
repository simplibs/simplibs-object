from typing import Any, TYPE_CHECKING
# Outers
from ...with_constant import with_constant
from ...with_composite import with_composite
from ...with_constants.vaidations import (
    validate_inner_tuple_is_tuple,
    validate_inner_tuple_has_length_two,
    validate_inner_tuple_name_is_str
)
# Inners
from .validations import raise_with_any_unknown_name
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.core_mixins import (
        InfrastructureProtocol,
        InfrastructuredComponent,
    )
    from ......_core.protocols.alias_typings import ChangeTuple


def process_single_change(
    self: "InfrastructureProtocol",
    change: "ChangeTuple",
) -> "InfrastructuredComponent":
    """
    Processes a single (name, value) change.
    Returns a new instance with the applied update.

    Integration requirement:
    The provided instance MUST inherit from:
      1. Snapshot (provides _restore_snapshot)
      2. NodesDicts (provides metadata and node access)
    Otherwise, the pipeline will raise AttributeError.
    """

    # 1. Validate tuple structure
    if (
        not isinstance(change, tuple)
        or len(change) != 2
        or not isinstance(change[0], str)
    ):
        validate_inner_tuple_is_tuple(self, change)
        validate_inner_tuple_has_length_two(self, change)
        validate_inner_tuple_name_is_str(self, change)

    name, value = change

    # 2. Constant update
    if name in self._constant_names_set:
        return with_constant(self, name, value)

    # 3. Composite update
    if name in self.meta.node_names_set:
        return with_composite(self, name, value)

    # 4. Unknown name
    raise_with_any_unknown_name(self, name, value)


_DESIGN_NOTES = """
# process_single_change

## Purpose
Handles a single `(name, value)` update in the immutability pipeline.
This function is the smallest routing unit of the `with_any` mechanism and
decides whether the update should be processed as a constant or composite
change.

It ensures that even the simplest update follows the full immutability rules.

## Architectural role
This function is used exclusively by:

- [with_any](ca://s?q=Explain_with_any) — mixed update pipeline

It provides the minimal dispatch logic for single-value updates.

## How it works
The function performs four deterministic steps:

### 1. Validate tuple structure
Ensures the input is a `(name, value)` pair with a string name.  
This prevents malformed updates from entering the immutability pipeline.

### 2. Route constant updates
If the name refers to a constant, the function delegates to  
[with_constant](ca://s?q=Explain_with_constant).

### 3. Route composite updates
If the name refers to a composite node, the function delegates to  
[with_composite](ca://s?q=Explain_with_composite).

### 4. Reject unknown names
If the name is neither a constant nor a composite, the update is invalid.

## Why this function exists
`with_any` must support both:

- single-value updates,  
- multi-value updates.

Instead of duplicating logic, `process_single_change` provides a clean,
minimal, and deterministic dispatch mechanism.

This separation improves:

- readability,  
- maintainability,  
- testability,  
- correctness.

## Deterministic behavior
The update is deterministic because:

- routing is based on canonical metadata (`_constant_names_set`, `node_names_set`),  
- delegated functions (`with_constant`, `with_composite`) are pure and stable,  
- validation prevents malformed updates.

## Integration requirements
The function assumes the instance implements:

- [Snapshot](ca://s?q=Explain_Snapshot_mixin) — provides `_restore_snapshot`  
- [NodesDicts](ca://s?q=Explain_NodesDicts_mixin) — provides node metadata  

Without these mixins, the pipeline cannot reconstruct the instance.

## Stability guarantee
Any change to this function would affect:

- routing logic in `with_any`,  
- immutability correctness,  
- debugging behavior,  
- serialization consistency.

Therefore, `process_single_change` is treated as a **core invariant** of the
immutability subsystem.

## Notes
- This function is intentionally minimal and side-effect-free.  
- It is not part of the public API; it is used internally by mixins.  
- All structural logic is delegated to metadata and helper functions.

"""