from typing import TYPE_CHECKING
# Inners
from ._collect_nested_inner_properties import _collect_nested_inner_properties
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.metadata import SimpleMetadataLike


def collect_all_nested_properties(
    meta: "SimpleMetadataLike"
) -> dict[str, property]:
    """
    Returns a dictionary of properties for all nested inner elements.
    Direct inners are ignored (they already have their own properties).
    """

    # 1. Initialize result container
    result = {}

    # 2. Iterate through direct inners
    for inner in meta.inners:

        # 2.1 Extract metadata
        inner_meta = inner.meta
        inner_meta: "SimpleMetadataLike"

        # 2.2 Process only composite inners
        if not inner_meta.is_constant:

            # 2.2.1 Build initial path tuple
            path = (inner_meta.name_private,)

            # 2.2.2 Recursively collect nested properties
            _collect_nested_inner_properties(inner_meta, path, result)

    # 3. Return collected properties
    return result


_DESIGN_NOTES = """
# collect_all_nested_properties

## Purpose
Collects properties for all *nested* inner elements of a composite structure.
Direct inners are intentionally skipped because they already have their own
properties generated during class initialization.

This function acts as the entry point for nested property discovery.

## Architectural role
`collect_all_nested_properties` is used by:

- `InnersPropertyMixin.__extend_instance_class__`
- metadata-driven property generation
- composite structure expansion
- debugging and introspection tools

It orchestrates the recursive property collection process by delegating the
actual traversal to `_collect_nested_inner_properties`.

## How it works
The function performs three deterministic steps:

### 1. Initialize result container
Creates an empty dictionary that will be filled with generated properties.

### 2. Iterate through direct inners
For each inner element in `meta.inners`:

- extracts its metadata,
- checks whether it is a composite (`not is_constant`),
- builds the initial path tuple,
- invokes the recursive collector.

Direct constants are skipped because they already have properties generated
by the core property builders.

### 3. Return collected properties
The final dictionary contains properties for all nested inner elements,
organized by their fully qualified names.

## Integration requirements
The function assumes:

- **SimpleMetadataLike**  
  Provides `.inners`, `.name_private`, `.is_constant`.

- **_collect_nested_inner_properties**  
  Performs the recursive traversal and property generation.

Without these components, nested property generation cannot operate correctly.

## Why this function exists
Composite structures can contain deeply nested inner elements.  
To expose them as Python properties, the system must:

- traverse metadata hierarchies,
- build stable access paths,
- generate properties deterministically,
- skip direct inners (already handled elsewhere),
- delegate recursion to a dedicated utility.

This function encapsulates the orchestration logic for that process.

## Deterministic behavior
The function guarantees:

- stable ordering based on metadata,
- predictable path construction,
- consistent skipping of direct inners,
- deterministic recursion entry points.

This determinism is essential for introspection, debugging, and composite
behavior.

## Stability guarantee
Any change to this function would affect:

- property generation,
- composite access behavior,
- metadata consistency,
- debugging tools,
- class initialization.

Therefore, `collect_all_nested_properties` is treated as a **core invariant**
of the property subsystem.

## Notes
- This function is intentionally minimal and side‑effect‑free.
- It is not part of the public API; it is used internally by mixins.
- All structural logic is delegated to metadata and recursive collectors.
"""